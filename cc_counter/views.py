
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.template import RequestContext, loader


from reviewboard.reviews.views import _find_review_request, _query_for_diff, get_patched_file, raw_diff
from reviewboard.diffviewer.diffutils import convert_to_unicode, get_original_file

from cc_counter.ccreader import analyze_file

import os

HOMEFOLDER = os.getenv('HOME')

def _download_ccdata(request, review_request_id, revision,
                        filediff_id, local_site=None, modified=True):
    """Generates the Cyclometric complexity of a specified file.

    This will download the file as a string, write it to a temporary file 
    in the homefolder, run the analysis, delete the temporary file, and 
    output the cyclometric complexity of the data followed by the file name.
    """

    review_request, response = \
        _find_review_request(request, review_request_id, local_site)

    if not review_request:
        return response

    draft = review_request.get_draft(request.user)
    diffset = _query_for_diff(review_request, request.user, revision, draft)
    filediff = get_object_or_404(diffset.files, pk=filediff_id)
    encoding_list = diffset.repository.get_encoding_list()
    data = get_original_file(filediff, request, encoding_list)

    if modified:
        data = get_patched_file(data, filediff, request)

    data = convert_to_unicode(data, encoding_list)[1]

    temp_file_name = "cctempfile_" + filediff.source_file
    source_file = os.path.join(HOMEFOLDER, temp_file_name)

    temp_file = open(source_file, 'w')
    temp_file.write(data)
    temp_file.close()
    ccdata = analyze_file(source_file)
    os.remove(source_file)
      
    if not ccdata:
    	ccdata = "Incompatable file type"

    return ccdata, filediff.source_file

def download_ccdata(request, review_request_id, revision,
                        filediff_id):
    """Generates the Cyclometric complexity of a specified file.

    This will download the file as a string, write it to a temporary file 
    in the homefolder, run the analysis, delete the temporary file, and 
    output the cyclometric complexity of the data followed by the file name.
    """

    ccdata, source_file = _download_ccdata(request, review_request_id, revision, filediff_id) 

    template = loader.get_template('cc_counter/download_ccdata.html')
    context = RequestContext(request, {
        'ccdata' : ccdata,
        'source_file' : source_file,
    })
    return HttpResponse(template.render(context))

def reviewrequest_cc(request, review_request_id):
    """The generic view of the Cyclometric complexity counter
    """

    """"To be finished"""
    
    return HttpResponse("unimplemented", content_type='text/plain; charset=utf-8')