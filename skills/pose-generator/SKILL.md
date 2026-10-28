---
name: pose-generator
description: Generate a pose image from a text description, a reference image, or both. Use for 文字描述生成姿势图、参考图片生成相似图片、姿势参考生图, text-to-image pose generation, or generating from a pose reference.
---

# Pose Generator

Generate one pose image from a text description, a reference image, or both. When a reference is supplied, preserve the requested visible attributes as closely as the image tool permits and apply the user's changes. When only text is supplied, create the requested image directly without requiring or inventing a reference. Do not promise an exact copy.

## Resolve inputs

1. Use the user's text description, supplied image, an image already clearly identified in the conversation, or a selected `pose-search` catalogue image. A sufficiently specific text-only request is enough to proceed. If neither a usable description nor an identifiable image is available, ask what pose or image the user wants. A `KF` number such as `KF001` is a permanent kungfu catalogue number: look it up as described below. An unqualified list number refers only to a numbered list already shown to the user; don't invent the mapping.
2. For a catalogue ID, use the `pose-search` search script when available: `python3 <repository>/shared/scripts/search.py --query <ID> --limit 1`. Check that the returned action ID or view ID exactly matches the requested ID and that `image_path` exists. The reference category contains WebP mannequin line drawings; do not describe them as photos. Other categories may use different media. If the catalogue is unavailable, ask the user for the reference image or a usable path.
   For a permanent kungfu number, run `python3 <repository>/shared/scripts/search.py --category kungfu --query KF001 --limit 5`, replacing `KF001` with the requested number. Confirm the exact number appears in the returned action's tags, use its action ID, and select the requested available angle. A request explicitly identifying kungfu number 1 may be normalized to `KF001`; do not reinterpret an unqualified list number. If the number or angle does not exist, say so rather than substituting another action or angle. The complete mapping is in `categories/kungfu/numbered-poses.md`.
3. If there is an image, inspect it when the tool requires it or when visual details must be described. Establish whether the user wants the whole image reproduced or only its pose. When the user asks to select a pose from an image, treat that image as a pose reference: by default, generate a new figure in the existing project catalogue's mannequin line-drawing style, rather than retaining the reference figure's appearance. Use `categories/reference/img/full_single_P015_front.webp` as a style reference when available; inspect it and pass it alongside the pose reference when the image tool supports both. The style is a clean black-line articulated mannequin on a white background, with visible joint markers and construction lines. Honor an explicitly requested style or subject instead. When the user asks to reproduce the whole reference image, retain its medium and appearance unless they request changes. Do not copy a mannequin's anatomy onto a different subject unless requested. If the request is text-only, use the description and make reasonable choices for unspecified nonessential details.

## Generate

- Call an available image-generation or image-editing tool with the user's text and any supplied reference image. When local paths are used, inspect each image first if the tool requires it; follow the tool's own rules for including reference images. If a requested reference or a suitable tool is unavailable, say so and offer a usable prompt instead of claiming that an image was generated.
- For an image reference, describe the visible pose precisely: body orientation, limb placement, hands, head direction, and camera angle where visible. For a selected pose, generate one new complete figure using the project style above; do not crop, enlarge, or isolate the original panel as the final result. Omit the source image's grid and labels unless requested. When reproducing an entire image, preserve its framing, background and style unless the user asks to change them. For text-only requests, use the stated pose and style; do not claim to have observed a reference image. Do not invent obscured details or assert that the generated subject is an exact match.
- Generate one image unless the user explicitly requests another number. Return the image and identify any reference or pose ID used. If the pose or other required attributes are materially wrong, say so and offer a retry.
- If the task is to place the same person in multiple different poses in a single image, use the `pose-transfer` skill when available.

## Source rights

The `reference` category's original images and data belong to ギア; the source project does not grant commercial reuse rights for those assets. Other categories have their own source information; consult their `source.md` and do not claim that using a reference grants a commercial license.
