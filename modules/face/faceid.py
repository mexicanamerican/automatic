from typing import List
import os
import cv2
import torch
import numpy as np
import diffusers
import huggingface_hub as hf
from PIL import Image
from modules import processing, shared, devices


FACEID_MODELS = {
    "FaceID Base": "h94/IP-Adapter-FaceID/ip-adapter-faceid_sd15.bin",
    "FaceID Plus v1": "h94/IP-Adapter-FaceID/ip-adapter-faceid-plus_sd15.bin",
    "FaceID Plus v2": "h94/IP-Adapter-FaceID/ip-adapter-faceid-plusv2_sd15.bin",
    "FaceID XL": "h94/IP-Adapter-FaceID/ip-adapter-faceid_sdxl.bin",
    # "FaceID Portrait v10": "h94/IP-Adapter-FaceID/ip-adapter-faceid-portrait_sd15.bin",
    # "FaceID Portrait v11": "h94/IP-Adapter-FaceID/ip-adapter-faceid-portrait-v11_sd15.bin",
    # "FaceID XL Plus v2": "h94/IP-Adapter-FaceID/ip-adapter-faceid_sdxl.bin",
}
faceid_model = None
faceid_model_name = None
debug = shared.log.trace if os.environ.get("SD_FACE_DEBUG", None) is not None else lambda *args, **kwargs: None


def face_id(
    p: processing.StableDiffusionProcessing,
    app,
    source_images: List[Image.Image],
    model: str,
    override: bool,
    cache: bool,
    scale: float,
    structure: float,
):
    global faceid_model, faceid_model_name  # pylint: disable=global-statement
    if source_images is None or len(source_images) == 0:
        shared.log.warning('FaceID: no input images')
        return None

    from insightface.utils import face_align
    try:
        from ip_adapter.ip_adapter_faceid import (
            IPAdapterFaceID,
            IPAdapterFaceIDPlus,
            IPAdapterFaceIDXL,
            IPAdapterFaceIDPlusXL,
        )
        from ip_adapter.ip_adapter_faceid_separate import (
            IPAdapterFaceID as IPAdapterFaceIDPortrait,
        )
    except Exception as e:
        shared.log.error(f"FaceID incorrect version of ip_adapter: {e}")
        return None

    ip_ckpt = FACEID_MODELS[model]
    folder, filename = os.path.split(ip_ckpt)
    basename, _ext = os.path.splitext(filename)
    model_path = hf.hf_hub_download(repo_id=folder, filename=filename, cache_dir=shared.opts.diffusers_dir)
    if model_path is None:
        shared.log.error(f"FaceID download failed: model={model} file={ip_ckpt}")
        return None
    if override:
        shared.sd_model.scheduler = diffusers.DDIMScheduler(
            num_train_timesteps=1000,
            beta_start=0.00085,
            beta_end=0.012,
            beta_schedule="scaled_linear",
            clip_sample=False,
            set_alpha_to_one=False,
            steps_offset=1,
        )
    shortcut = None
    if faceid_model is None or faceid_model_name != model or not cache:
        shared.log.debug(f"FaceID load: model={model} file={ip_ckpt}")
        if "XL Plus" in model:
            image_encoder_path = "laion/CLIP-ViT-H-14-laion2B-s32B-b79K"
            faceid_model = IPAdapterFaceIDPlusXL(
                sd_pipe=shared.sd_model,
                image_encoder_path=image_encoder_path,
                ip_ckpt=model_path,
                lora_rank=128,
                num_tokens=4,
                device=devices.device,
                torch_dtype=devices.dtype,
            )
        elif "XL" in model:
            faceid_model = IPAdapterFaceIDXL(
                sd_pipe=shared.sd_model,
                ip_ckpt=model_path,
                lora_rank=128,
                num_tokens=4,
                device=devices.device,
                torch_dtype=devices.dtype,
            )
        elif "Plus" in model:
            image_encoder_path = "laion/CLIP-ViT-H-14-laion2B-s32B-b79K"
            faceid_model = IPAdapterFaceIDPlus(
                sd_pipe=shared.sd_model,
                image_encoder_path=image_encoder_path,
                ip_ckpt=model_path,
                lora_rank=128,
                num_tokens=4,
                device=devices.device,
                torch_dtype=devices.dtype,
            )
        elif "Portrait" in model:
            faceid_model = IPAdapterFaceIDPortrait(
                sd_pipe=shared.sd_model,
                ip_ckpt=model_path,
                num_tokens=16,
                n_cond=5,
                device=devices.device,
                torch_dtype=devices.dtype,
            )
        else:
            faceid_model = IPAdapterFaceID(
                sd_pipe=shared.sd_model,
                ip_ckpt=model_path,
                lora_rank=128,
                num_tokens=4,
                device=devices.device,
                torch_dtype=devices.dtype,
            )
        shortcut = "v2" in model
        faceid_model_name = model
    else:
        shared.log.debug(f"FaceID cached: model={model} file={ip_ckpt}")

    processed_images = []
    face_embeds = []
    face_images = []
    for i, source_image in enumerate(source_images):
        np_image = cv2.cvtColor(np.array(source_image), cv2.COLOR_RGB2BGR)
        faces = app.get(np_image)
        if len(faces) == 0:
            shared.log.error("FaceID: no faces found")
            break
        face_embeds.append(torch.from_numpy(faces[0].normed_embedding).unsqueeze(0))
        face_images.append(face_align.norm_crop(np_image, landmark=faces[0].kps, image_size=224))
        shared.log.debug(f'FaceID face: i={i+1} score={faces[0].det_score:.2f} gender={"female" if faces[0].gender==0 else "male"} age={faces[0].age} bbox={faces[0].bbox}')
        p.extra_generation_params[f"FaceID {i+1}"] = f'{faces[0].det_score:.2f} {"female" if faces[0].gender==0 else "male"} {faces[0].age}y'
    if len(face_embeds) == 0:
        shared.log.error("FaceID: no faces found")
        return None
    face_embeds = torch.cat(face_embeds, dim=0)

    ip_model_dict = {  # main generate dict
        "num_samples": p.batch_size,
        "width": p.width,
        "height": p.height,
        "num_inference_steps": p.steps,
        "scale": scale,
        "guidance_scale": p.cfg_scale,
        "faceid_embeds": face_embeds.shape,  # placeholder
    }
    # optional generate dict
    if shortcut is not None:
        ip_model_dict["shortcut"] = shortcut
    if "Plus" in model:
        ip_model_dict["s_scale"] = structure
    shared.log.debug(f"FaceID args: {ip_model_dict}")
    if "Plus" in model:
        ip_model_dict["face_image"] = face_images
    ip_model_dict["faceid_embeds"] = face_embeds # overwrite placeholder
    # run generate
    faceid_model.set_scale(scale)
    for i in range(p.n_iter):
        ip_model_dict.update({
                "prompt": p.all_prompts[i],
                "negative_prompt": p.all_negative_prompts[i],
                "seed": int(p.all_seeds[i]),
            })
        debug(f"FaceID: {ip_model_dict}")
        res = faceid_model.generate(**ip_model_dict)
        if isinstance(res, list):
            processed_images += res
    faceid_model.set_scale(0)

    if not cache:
        faceid_model = None
        faceid_model_name = None
    devices.torch_gc()

    p.extra_generation_params["IP Adapter"] = f"{basename}:{scale}"
    return processed_images
