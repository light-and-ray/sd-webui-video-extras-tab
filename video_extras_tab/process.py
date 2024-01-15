import os
from modules.ui import plaintext_to_html
from modules import progress, shared
import datetime
from video_extras_tab.video_tools import getVideoFrames, save_video

extrasModeIdx = 0
inputDirIdx = 3
outputDirIdx = 4
showExtrasResultsIdx = 5




def process(taskId, pathIn, fps, pathOut, extrasSubbmit, *args, **kwargs):
    restoreOpts = None
    try:
        tabIndex = args[extrasModeIdx]
        if tabIndex != 3: # video
            return extrasSubbmit(taskId, *args, **kwargs)

        shared.total_tqdm.clear()
        shared.state.textinfo = 'video preparing'
        timestamp = int(datetime.datetime.now().timestamp())
        args = list(args)

        if pathOut == "":
            pathOut = os.path.join(os.path.dirname(pathIn), f'out_{timestamp}')
        else:
            pathOut = os.path.join(pathOut, f'out_{timestamp}')
        if os.path.exists(pathOut):
            for file in os.listdir(pathOut):
                if file.endswith(f'.{shared.opts.samples_format}'):
                    os.remove(os.path.join(pathOut, file))
        temp_folder, fps_in, fps_out = getVideoFrames(pathIn, fps)

        args[inputDirIdx] = temp_folder
        args[outputDirIdx] = pathOut
        args[extrasModeIdx] = 2 # batch from dir
        toRestore_opt1 = shared.opts.use_original_name_batch
        toRestore_opt2 = shared.opts.use_upscaler_name_as_suffix
        toRestore_opt3 = shared.opts.live_previews_enable
        def restoreOpts_():
            shared.opts.use_original_name_batch = toRestore_opt1
            shared.opts.use_upscaler_name_as_suffix = toRestore_opt2
            shared.opts.live_previews_enable = toRestore_opt3
        restoreOpts = restoreOpts_
        shared.opts.use_original_name_batch = False
        shared.opts.use_upscaler_name_as_suffix = False
        shared.opts.live_previews_enable = False # crashes if True

        _, _, html_comment, = extrasSubbmit(taskId, *args, **kwargs)

        shared.state.textinfo = 'video saving'
        print("generate done, generating video")
        save_video_path = os.path.join(pathOut, f'output_{os.path.basename(pathIn)}_{timestamp}.mp4')
        save_video(pathOut, fps_out, pathIn, save_video_path)

        return [], plaintext_to_html(f"Saved into {save_video_path}"), html_comment
    finally:
        progress.finish_task(taskId)
        if restoreOpts:
            restoreOpts()



    

