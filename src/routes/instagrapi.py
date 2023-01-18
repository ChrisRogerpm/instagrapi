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


@main.route('/uploadStoryVideo', methods=['POST'])
def uploadStoryVideo():
    message = ''
    status = False
    try:
        req = InstagrapiService.setParameters(request)
        InstagrapiService.uploadStoryVideo(req)
        status = True
        message = 'Video to Story Uploaded'
    except (Exception, ValueError) as ex:
        message = str(ex)
    return jsonify({
        'status': status,
        'message': message
    })


@main.route('/uploadStoryPhoto', methods=['POST'])
def uploadStoryPhoto():
    message = ''
    status = False
    try:
        req = InstagrapiService.setParameters(request)
        InstagrapiService.uploadStoryPhoto(req)
        status = True
        message = 'Photo to Story Uploaded'
    except (Exception, ValueError) as ex:
        message = str(ex)
    return jsonify({
        'status': status,
        'message': message
    })
