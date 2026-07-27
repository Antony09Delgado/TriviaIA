from moviepy import VideoFileClip, ColorClip, CompositeVideoClip
from moviepy.video.fx import MaskColor

VIDEO_PATH = r"C:\Users\Antony\Desktop\Trivia\marca\IMG_7823.MOV"

clip = VideoFileClip(VIDEO_PATH)
clip = clip.subclipped(0, min(5, clip.duration))

# Quita un fondo verde/cian usando una máscara.
clip_transparente = clip.with_effects([
    MaskColor(color=[0, 130, 62], threshold=100, stiffness=8),
])

# Para previsualizar, colocamos el video sobre un fondo negro.
background = ColorClip(size=clip.size, color=(0, 0, 0), duration=clip_transparente.duration)
preview_clip = CompositeVideoClip([
    background,
    clip_transparente.with_position("center"),
])

preview_clip.preview(fps=24)