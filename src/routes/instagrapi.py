from flask import Blueprint, jsonify, request

from utils.InstagrapiService import InstagrapiService

main = Blueprint('instagrapi_blueprint', __name__)


@main.route('/uploadPhoto', methods=['POST'])
def uploadPhoto():
    message = ''
    status = False
    try:
        req = InstagrapiService.setParameters(request)
        InstagrapiService.uploadPhoto(req)
        status = True
        message = 'Photo Uploaded'
    except (Exception, ValueError) as ex:
        message = str(ex)
    return jsonify({
        'status': status,
        'message': message
    })


@main.route('/uploadVideo', methods=['POST'])
def uploadVideo():
    message = ''
    status = False
    try:
        req = InstagrapiService.setParameters(request)
        InstagrapiService.uploadVideo(req)
        status = True
        message = 'Video Uploaded'
    except (Exception, ValueError) as ex:
        message = str(ex)
    return jsonify({
        'status': status,
        'message': message
    })


@main.route('/uploadStoryPhotoVideo', methods=['POST'])
def uploadStoryPhotoVideo():
    message = ''
    status = False
    try:
        req = InstagrapiService.setParameters(request)
        InstagrapiService.uploadStoryPhotoVideo(req)
        status = True
        message = 'Story Uploaded'
    except (Exception, ValueError) as ex:
        message = str(ex)
    return jsonify({
        'status': status,
        'message': message
    })


@main.route('/searchFont')
def searchFont():
    data = []
    message = ""
    try:
        req = request.form
        data = InstagrapiService.searchFont(req['font'])
    except (Exception) as ex:
        message = str(ex)
    return jsonify({
        'data': data,
        'message': message
    })
