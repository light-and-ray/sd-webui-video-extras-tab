from modules.ui import plaintext_to_html
from modules import progress

extrasModeIdx = 0
inputDirIdx = 3
outputDifIdx = 4
showExtrasResultsIdx = 5




def process(taskId, pathIn, fps, pathOut, extrasSubbmit, *args, **kwargs):
    tabIndex = args[extrasModeIdx]
    print('!!!', tabIndex, pathIn, fps, pathOut)
    if tabIndex != 3:
        return extrasSubbmit(taskId, *args, **kwargs)
    
    progress.finish_task(taskId)
    # result_images, html_info_x, html_log = extrasSubbmit(taskId, *args, **kwargs)
    return [], plaintext_to_html('video tab completed'), ''

