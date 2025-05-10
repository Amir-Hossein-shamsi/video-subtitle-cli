#!/usr/bin/env python3
"""
A command-line tool to extract audio, transcribe with Whisper, and embed subtitles.
"""
import subprocess
import argparse
import os
import whisper
import json

def extract_audio(input_file, output_file, codec='wav', stream_index=0, quality=None, bitrate=None):
    """Extract audio from a video file using FFmpeg."""
    cmd = ['ffmpeg', '-y', '-i', input_file, '-vn', '-map', f'0:a:{stream_index}']

    if codec == 'copy':
        cmd += ['-c:a', 'copy']
    elif codec == 'mp3':
        cmd += ['-c:a', 'libmp3lame']
        if quality is not None:
            cmd += ['-q:a', str(quality)]
    elif codec == 'aac':
        cmd += ['-c:a', 'aac']
        if bitrate:
            cmd += ['-b:a', bitrate]
    elif codec == 'wav':
        cmd += ['-c:a', 'pcm_s16le']
    else:
        raise ValueError(f"Unsupported codec: {codec}")

    cmd.append(output_file)
    subprocess.run(cmd, check=True)
    print(f"✅ Audio extracted to {output_file}")


def transcribe(audio_path, model_name,lang='en'):
    """Transcribe audio with Whisper and generate SRT, TXT, JSON outputs."""
    model = whisper.load_model(model_name)
    result = model.transcribe(audio_path,language=lang, temperature=0.0,without_timestamps=False)
    segments = []
    for i, seg in enumerate(result['segments']):
        segments.append({
            'id': i,
            'start': seg['start'],
            'end': seg['end'],
            'text': seg['text'].strip()
        })

    base = os.path.splitext(audio_path)[0]
    json_path = base + '_output.json'
    srt_path = base + '.srt'
    txt_path = base + '.txt'

    # JSON
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump({'segments': segments}, f, indent=4, ensure_ascii=False)

    # SRT
    def fmt(ts):
        h = int(ts // 3600)
        m = int((ts % 3600) // 60)
        s = ts % 60
        return f"{h:02d}:{m:02d}:{s:06.3f}".replace('.', ',')

    with open(srt_path, 'w', encoding='utf-8') as f:
        for seg in segments:
            f.write(f"{seg['id'] + 1}\n")
            f.write(f"{fmt(seg['start'])} --> {fmt(seg['end'])}\n")
            f.write(f"{seg['text']}\n\n")

    # TXT
    with open(txt_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(seg['text'] for seg in segments))

    print(f"✅ Transcription saved: {json_path}, {srt_path}, {txt_path}")
    return srt_path

def embed_subtitles(input_video, srt_file, output_video, lang='eng'):
    """Embed subtitles into a video file using FFmpeg."""
    cmd = [
        'ffmpeg', '-y', '-i', input_video, '-i', srt_file,
        '-c:v', 'copy', '-c:a', 'copy', '-c:s', 'mov_text',
        '-map', '0', '-map', '1',
        '-metadata:s:s:0', f'language={lang}',
        output_video
    ]
    subprocess.run(cmd, check=True)
    print(f"✅ Subtitled video saved to {output_video}")


def main():
    parser = argparse.ArgumentParser(description='Extract, transcribe, and embed subtitles into a video.')
    parser.add_argument('--input', '-i', required=True, help='Input video file (e.g., .mp4)')
    parser.add_argument('--output-dir', '-o', default='.output/', help='Directory for outputs')
    parser.add_argument('--codec', default='wav', choices=['copy','mp3','aac','wav'], help='Audio codec')
    parser.add_argument('--quality', type=int, help='MP3 quality (0=best,9=worst)')
    parser.add_argument('--bitrate', help='AAC bitrate (e.g., 192k)')
    parser.add_argument('--model', default='small', help='Whisper model size (tiny, base, small, medium, large)')
    parser.add_argument('--lang', default='eng', help='Subtitle language code')
    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)
    base_name = os.path.splitext(os.path.basename(args.input))[0]
    audio_file = os.path.join(args.output_dir, f"{base_name}.wav") if args.codec=='wav' else os.path.join(args.output_dir, f"{base_name}.{args.codec}")

    extract_audio(args.input, audio_file, codec=args.codec, quality=args.quality, bitrate=args.bitrate)
    srt_path = transcribe(audio_file, args.model,lang=args.lang)
    video_out = os.path.join(args.output_dir, f"{base_name}_subbed.mp4")
    embed_subtitles(args.input, srt_path, video_out, lang=args.lang)

if __name__ == '__main__':
    main()
