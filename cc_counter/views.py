
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.template import RequestContext, loader


from reviewboard.reviews.views import _find_review_request, _query_for_diff, get_patched_file, raw_diff
from reviewboard.diffviewer.diffutils import convert_to_unicode, get_original_file

from cc_counter.ccreader import analyze_file, get_comparison_data
from cc_counter.cccomparer import track_diff_ccchanges

import os

HOMEFOLDER = os.getenv('HOME')

def _download_analysis(request, analyze_function, review_request_id, revision,
                        filediff_id, local_site=None, modified=True):
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
    data_analysis = analyze_function(source_file)
    os.remove(source_file)
      
    if not comparison_data:
        comparison_data = None

    return filediff.source_file, comparison_data 


def _download_comparison_data(request, review_request_id, revision,
                        filediff_id, local_site=None, modified=True):
    """Generates the Cyclometric complexity of a specified file.

    This will download the file as a string, write it to a temporary file 
    in the homefolder, run the analysis, delete the temporary file, and 
    outputs a tuple of cyclometric complexity of the data (dictionary), and
    the file name (string).
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
    comparison_data = get_comparison_data(source_file)
    os.remove(source_file)
      
    if not comparison_data:
        comparison_data = None

    return filediff.source_file, comparison_data 

def _download_ccdata(request, review_request_id, revision,
                        filediff_id, local_site=None, modified=True):
    """Generates the Cyclometric complexity of a specified file.

    This will download the file as a string, write it to a temporary file 
    in the homefolder, run the analysis, delete the temporary file, and 
    outputs a tuple of cyclometric complexity of the data (dictionary), and
    the file name (string).
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

    return filediff.source_file, ccdata 

def download_ccdata(request, review_request_id, revision,
                        filediff_id):
    """Generates the Cyclometric complexity of a specified file as view.

    Calls on _download_ccdata and simply packages the outputs into a view
    """

    source_file, ccdata = _download_ccdata(request, review_request_id, revision, filediff_id) 

    template = loader.get_template('cc_counter/download_ccdata.html')
    context = RequestContext(request, {
        'ccdata' : ccdata,
        'source_file' : source_file,
    })
    return HttpResponse(template.render(context))

def _reviewrequest_recent_cc(request, review_request_id, revision_offset=0,
                                local_site=None, modified=True):

    review_request, response = \
        _find_review_request(request, review_request_id, local_site)

    if not review_request:
        return response

    draft = review_request.get_draft(request.user)
    diffset = _query_for_diff(review_request, request.user, None, draft)
    
    revision = diffset.revision

    if revision - revision_offset <= 0:
        return [revision - revision_offset]
    else:
        revision -=  revision_offset
        diffset = _query_for_diff(review_request, request.user, revision, draft)
        
    filediff_ids = [ffile.pk for ffile in diffset.files.all()] 

    reviewrequest_ccdata = dict()
    for filediff_id in filediff_ids:
        filename, comparison_data = _download_comparison_data(request, review_request_id, revision, filediff_id)
        reviewrequest_ccdata[filename] = comparison_data
        
    return reviewrequest_ccdata


def reviewrequest_recent_cc(request, review_request_id, revision_offset=1):
    """The generic view of the Cyclometric complexity counter
    """

    """"To be finished"""
    
    reviewrequest_ccdata = _reviewrequest_recent_cc(request, review_request_id)
    prev_reviewrequest_ccdata = _reviewrequest_recent_cc(request, review_request_id, revision_offset=1)
    diff_changes = track_diff_ccchanges(reviewrequest_ccdata, prev_reviewrequest_ccdata)

    compatable_files = []
    incompatable_files = []

    for diff_change in diff_changes:
        if diff_change['ccchanges'] == None:
            incompatable_files += [diff_change]
        else:
            compatable_files += [diff_change]

    for c_file in compatable_files:
        for types in c_file['ccchanges']:
            c_file['ccchanges'][types] = [cc.dict_form() for cc in c_file['ccchanges'][types]]


    template = loader.get_template('cc_counter/reviewrequest_recent_cc.html')
    context = RequestContext(request, {
        'incompatable_files': incompatable_files,
        'compatable_files': compatable_files
    })

    return HttpResponse(template.render(context))
