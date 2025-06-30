import os
from modules import shared, devices, sd_models, model_quant

debug = shared.log.trace if os.environ.get('SD_LOAD_DEBUG', None) is not None else lambda *args, **kwargs: None


def load_omnigen2(checkpoint_info, diffusers_load_config={}): # pylint: disable=unused-argument
    repo_id = sd_models.path_to_repo(checkpoint_info.name)

    from modules.omnigen2 import OmniGen2Pipeline, OmniGen2Transformer2DModel, Qwen2_5_VLForConditionalGeneration
    import diffusers
    from diffusers import pipelines
    diffusers.OmniGen2Pipeline = OmniGen2Pipeline # monkey-pathch
    pipelines.auto_pipeline.AUTO_TEXT2IMAGE_PIPELINES_MAPPING["omnigen2"] = diffusers.OmniGen2Pipeline
    pipelines.auto_pipeline.AUTO_IMAGE2IMAGE_PIPELINES_MAPPING["omnigen2"] = diffusers.OmniGen2Pipeline
    pipelines.auto_pipeline.AUTO_INPAINT_PIPELINES_MAPPING["omnigen2"] = diffusers.OmniGen2Pipeline

    load_config, quant_config = model_quant.get_dit_args(diffusers_load_config, module='Model')
    transformer = OmniGen2Transformer2DModel.from_pretrained(
        repo_id,
        subfolder="transformer",
        cache_dir=shared.opts.diffusers_dir,
        trust_remote_code=True,
        **load_config,
        **quant_config,
    )

    load_config, quant_config = model_quant.get_dit_args(diffusers_load_config, module='TE')
    mllm = Qwen2_5_VLForConditionalGeneration.from_pretrained(
        repo_id,
        subfolder="mllm",
        cache_dir=shared.opts.diffusers_dir,
        trust_remote_code=True,
        **load_config,
        **quant_config,
    )

    pipe = OmniGen2Pipeline.from_pretrained(
        repo_id,
        # transformer=transformer,
        mllm=mllm,
        cache_dir=shared.opts.diffusers_dir,
        trust_remote_code=True,
        **load_config,
    )
    pipe.transformer = transformer # for omnigen2 transformer must be loaded after pipeline

    devices.torch_gc(force=True)
    return pipe
