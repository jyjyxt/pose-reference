---
name: pose-transfer
description: Turn one person or character photo into a single image showing 1–9 different poses, using pose references, pose IDs, or descriptions. Use for 一张照片生成多个姿势、换动作、姿势迁移、人物多动作拼图, pose transfer or a multi-pose character sheet. Default to five poses when the user does not choose a count.
---

# Pose Transfer

Create one image of the same subject in multiple poses. The source photo supplies the person's identity and appearance; pose references supply body and hand positions, not the reference figure's identity, body shape, clothing or visual style.

## Understand the request

The accompanying shared catalogue currently contains mannequin line drawings rather than finished photographs; other categories may be empty. It has full-body standing, sitting, crouching, kneeling and lying poses; upper-body gestures such as heart and V signs; and a separate adult-oriented intimate two-person section. Each pose may have several camera angles. Do not assume that it provides every type of couple pose or a photographic example.

Select according to the user's purpose:

- Photo or social-media ideas: prioritize natural poses that match the user's requested setting and body framing.
- Portrait, selfie or expression sheet: prioritize upper-body and hand gestures; don't force full-body framing.
- Drawing, character design or AI-image reference: prioritize clear silhouettes and requested body positions or angles.
- Specific pose, ID, or previously presented action number: honor that choice. A number only means the numbered list already shown in this conversation; never silently reinterpret it as a catalogue ID or a new list index.
- Two-person or intimate poses: the existing pair section is adult-oriented, and one portrait does not identify a second person. Do not invent a partner or treat the pair section as a general couple-posing library. Ask for the missing person or intended partner description when required and comply with the applicable image tool's content rules.

## Choose poses

1. Obtain the subject's photo from the conversation or a user-provided local path; if missing, ask for it. Respect the user's stated setting, framing, clothing, and pose choices. If the user specifies a single pose, use one; if they specify several, use exactly those. If no count or specific poses are supplied, use **five** varied suitable poses. Maximum: **nine poses in one result**. For a request exceeding nine, ask which up to nine to use.
2. Find actual references through the shared catalogue. Run `python3 <repository>/skills/pose-transfer/scripts/select_poses.py` for five varied references; `--count 1..9`, `--framing full|upper|mixed` and repeated `--id ID` select the requested count, framing or exact IDs. Results include stable numbers and local WebP paths. Use `python3 <repository>/shared/scripts/search.py` to find categories, phases and angles; pass the chosen IDs to the selector. Default searches exclude adult-labelled catalogue entries; only include them for an explicitly adult request and within applicable policy. The selector requires the accompanying shared catalogue and images.
3. If the user has not picked poses, select matching results without demanding unnecessary confirmation. Keep a stable list of the chosen IDs and their local reference paths, and identify them in the response. If the user gives an unresolved action number, show a numbered preview list with IDs and ask which to use. Never invent a catalogue entry. If the catalogue is unavailable, use the user's pose images or descriptions; otherwise explain what is missing.

## Produce the image

- Use an available image-generation or image-editing tool. Inspect local input images when the tool requires it. Label the source as the identity reference and each selected pose as a pose reference. If the tool cannot accept all reference images together, first combine the chosen poses into a single reference sheet, then supply the source photo and that sheet together. For catalogue poses, run `python3 <repository>/skills/pose-transfer/scripts/build_pose_sheet.py --output <new-file.png> --count 9 --framing full`, or pass repeated `--id ID` arguments in the selected order. The script requires ffmpeg and returns the panel-to-ID mapping. For user-supplied references use an equivalent deterministic collage tool. Inspect the sheet and preserve its panel order in the prompt. If a reference sheet cannot be created or the tool cannot use both images, explain the limitation; do not silently substitute textual descriptions for the requested image references.
- Make exactly one image-generation call for the complete composite, so all poses share one generation context. Do not generate individual panels separately and stitch them afterward. A single call supports consistency but does not guarantee it.
- Produce **one** output image. For multiple poses, use one clear panel per pose, laid out in reading order; five poses means exactly five panels, nine poses means a 3×3 grid. Do not add duplicate poses, extra people, labels, or empty frames. A single requested pose produces one ordinary image.
- Match each pose's visible limb placement, body direction and camera angle. Keep the same recognizable person, hairstyle, body characteristics, clothes and visual style across panels as far as the source allows. Preserve the source setting unless the user asks for a change. A cropped source may require inferred non-visible clothing or body details: avoid claiming those details were observed. Do not promise perfect identity or pose fidelity.
- Return the image and list which chosen pose occupies each panel. If the output is missing panels or differs materially from the requested poses, report it and offer a retry.

## Source rights

The reference category images and original data belong to ギア; the source project does not grant commercial reuse rights for those assets. For every category, consult its source information and do not imply a commercial license for the output.
