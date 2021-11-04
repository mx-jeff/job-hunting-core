from jobhunting.Models.apinfo import Apinfo


def searchApinfo(job='python'):
    apinfo = Apinfo()
    apinfo.searchJob(job)
    apinfo.selectJob()
    # apinfo.subscribeJob()
    apinfo.wait()
    # apinfo.close()
