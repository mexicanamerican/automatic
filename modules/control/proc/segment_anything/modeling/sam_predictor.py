from typing import Dict, List

import torch
from torch import nn

from .image_encoder import ImageEncoderViT
from .mask_decoder import MaskDecoder
from .prompt_encoder import PromptEncoder
from .tiny_vit_sam import TinyViT


class SamPredictor:
    def __init__(self):
        self.image_encoder = ImageEncoderViT()
        self.prompt_encoder = PromptEncoder()
        self.mask_decoder = MaskDecoder()

    def predict_masks(self, batched_input: List[Dict[str, torch.Tensor]], multimask_output: bool) -> List[Dict[str, torch.Tensor]]:
        predictions = []
        for input_data in batched_input:
            image = input_data['image']
            original_size = input_data['original_size']
            point_coords = input_data['point_coords']
            point_labels = input_data['point_labels']
            boxes = input_data['boxes']
            mask_inputs = input_data['mask_inputs']

            # Encode the image and prompts
            image_features = self.image_encoder(image)
            prompt_features = self.prompt_encoder(point_coords, point_labels)

            # Decode the masks
            masks, iou_predictions, low_res_logits = self.mask_decoder(image_features, prompt_features, boxes, mask_inputs, multimask_output)

            # Resize the masks to the original size
            masks = nn.functional.interpolate(masks, size=original_size, mode='bilinear', align_corners=False)

            # Append the predictions to the list
            predictions.append({
                'masks': masks,
                'iou_predictions': iou_predictions,
                'low_res_logits': low_res_logits
            })

        return predictions
