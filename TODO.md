# TODO

Main ToDo list can be found at [GitHub projects](https://github.com/users/vladmandic/projects)

## Current

## Future Candidates

- Refactor: Move `model_*` stuff into subfolder  
- Refactor: sampler options  
- Common repo for `T5` and `CLiP`  
- Upgrade: unblock `numpy`: see `gradio`
- Upgrade: unblock `pydantic`: see <https://github.com/Cschlaefli/automatic>

### Complete Features

- Python==3.13 improved support  
- Video: API support  
- LoRA: add OMI format support for SD35/FLUX.1  

### Under Consideration

- [IPAdapter negative guidance](https://github.com/huggingface/diffusers/discussions/7167)  
- [IPAdapter composition](https://huggingface.co/ostris/ip-composition-adapter)  
- [Refactor attention](https://github.com/huggingface/diffusers/pull/11311)  
- [STG](https://github.com/huggingface/diffusers/blob/main/examples/community/README.md#spatiotemporal-skip-guidance)  
- [LBM](https://github.com/gojasper/LBM)  
- [SmoothCache](https://github.com/huggingface/diffusers/issues/11135)  
- [MagCache](https://github.com/lllyasviel/FramePack/pull/673/files)
- [HiDream GGUF](https://github.com/huggingface/diffusers/pull/11550)  
- [Diffusers guiders](https://github.com/huggingface/diffusers/pull/11311)  
- [Nunchaku PulID](https://github.com/mit-han-lab/nunchaku/pull/274)  
- [Dream0 guidance](https://huggingface.co/ByteDance/DreamO)  
- [S3Diff diffusion upscaler](https://github.com/ArcticHare105/S3Diff)  
- [SUPIR upscaler](https://github.com/Fanghua-Yu/SUPIR)  

### Monitoring

- [TensorRT](https://github.com/huggingface/diffusers/pull/11173)

### New models

#### Stable
- [Diffusers-0.34.0](https://github.com/huggingface/diffusers/releases/tag/v0.34.0)  
- [WanAI-2.1 VACE](https://huggingface.co/Wan-AI/Wan2.1-VACE-14B)(https://github.com/huggingface/diffusers/pull/11582)  
- [LTXVideo-0.9.7](https://github.com/Lightricks/LTX-Video?tab=readme-ov-file#diffusers-integration)(https://github.com/huggingface/diffusers/pull/11516)  
- [Cosmos-Predict2-Video](https://huggingface.co/nvidia/Cosmos-Predict2-2B-Video2World)(https://github.com/huggingface/diffusers/pull/11695)  
#### Pending
- [Magi](https://github.com/SandAI-org/MAGI-1)(https://github.com/huggingface/diffusers/pull/11713)  
- [SEVA](https://github.com/huggingface/diffusers/pull/11440)  
- [SkyReels-v2](https://github.com/SkyworkAI/SkyReels-V2)(https://github.com/huggingface/diffusers/pull/11518)  
#### External:Unified/MultiModal
- [Bagel](https://huggingface.co/ByteDance-Seed/BAGEL-7B-MoT)(https://github.com/bytedance-seed/bagel)  
- [Ming](https://github.com/inclusionAI/Ming)  
- [Liquid](https://github.com/FoundationVision/Liquid)  
#### External:Image2Image/Editing
- [Step1X](https://github.com/stepfun-ai/Step1X-Edit)  
- [SD3 UltraEdit](https://github.com/HaozheZhao/UltraEdit)  
#### External:Video
- [WAN2GP](https://github.com/deepbeepmeep/Wan2GP)  
- [SelfForcing](https://github.com/guandeh17/Self-Forcing)  
- [DiffusionForcing](https://github.com/kwsong0113/diffusion-forcing-transformer)  
- [LanDiff](https://github.com/landiff/landiff)  
- [HunyuanCustom](https://github.com/Tencent-Hunyuan/HunyuanCustom)  
- [HunyuanAvatar](https://huggingface.co/tencent/HunyuanVideo-Avatar)  
- [WAN-CausVid](https://huggingface.co/lightx2v/Wan2.1-T2V-14B-CausVid)  
- [WAN-CausVid-Plus t2v](https://github.com/goatWu/CausVid-Plus/)  
- [WAN-StepDistill](https://huggingface.co/lightx2v/Wan2.1-T2V-14B-StepDistill-CfgDistill)  

## Code TODO

> pnpm lint | grep W0511 | awk -F'TODO ' '{print "- "$NF}' | sed 's/ (fixme)//g'
 
- control: support scripts via api
- fc: autodetect distilled based on model
- fc: autodetect tensor format based on model
- hypertile: vae breaks when using non-standard sizes
- install: enable ROCm for windows when available
- loader: load receipe
- loader: save receipe
- lora: add other quantization types
- lora: add t5 key support for sd35/f1
- lora: maybe force imediate quantization
- model load: force-reloading entire model as loading transformers only leads to massive memory usage
- model loader: implement model in-memory caching
- modernui: monkey-patch for missing tabs.select event
- modules/lora/lora_extract.py:188:9: W0511: TODO: lora: support pre-quantized flux
- nunchaku: batch support
- nunchaku: cache-dir for transformer and t5 loader
- processing: remove duplicate mask params
- resize image: enable full VAE mode for resize-latent
