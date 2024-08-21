import os
from modules.ui import plaintext_to_html
from modules import shared
from modules.postprocessing import run_postprocessing
import datetime
from video_extras_tab.video_tools import getVideoFrames, save_video, convertIntoPath, interrupted

videoTabIndex = 652

extrasModeIdx = 0
inputDirIdx = 3
outputDirIdx = 4
showExtrasResultsIdx = 5



def process(taskId, pathsIn, fps, originlPathOut, enableLivePreview, *args, **kwargs):
    restoreList = []
    try:
        if args[extrasModeIdx] != videoTabIndex:
            return run_postprocessing(*args, **kwargs)

        shared.total_tqdm.clear()
        shared.state.textinfo = 'video preparing'

        toRestore_opt1 = shared.opts.use_original_name_batch
        toRestore_opt2 = shared.opts.use_upscaler_name_as_suffix
        toRestore_opt3 = shared.opts.live_previews_enable
        def restoreOpts_():
            shared.opts.use_original_name_batch = toRestore_opt1
            shared.opts.use_upscaler_name_as_suffix = toRestore_opt2
            shared.opts.live_previews_enable = toRestore_opt3
        restoreList.append(restoreOpts_)
        shared.opts.use_original_name_batch = False
        shared.opts.use_upscaler_name_as_suffix = False
        shared.opts.live_previews_enable = enableLivePreview


        args = list(args)
        originlPathOut = convertIntoPath(originlPathOut)
        save_video_paths = []

        for pathIn in pathsIn.split('\n'):
            pathIn = convertIntoPath(pathIn)
            if not pathIn or pathIn.startswith('#'): continue
            pathOut = originlPathOut
            timestamp = int(datetime.datetime.now().timestamp())

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
            args[showExtrasResultsIdx] = False

            run_postprocessing(*args, **kwargs)

            shared.state.textinfo = 'video saving'
            save_video_path = os.path.join(pathOut, f'output_{os.path.basename(pathIn)}_{timestamp}.mp4')
            if len(save_video_path) > 260:
                save_video_path = os.path.join(pathOut, f'output_{timestamp}.mp4')
            save_video(pathOut, fps_out, pathIn, save_video_path)
            save_video_paths.append(save_video_path)
            if interrupted(): break

        return [], plaintext_to_html(f"Saved into {save_video_paths}"), ''
    finally:
        for restore in restoreList:
            restore()





