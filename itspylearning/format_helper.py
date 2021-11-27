def formatMessage(message): 
    formatted = {
        "id": message['MessageId'],
        "threadId": message['MessageThreadId'],
        "created": message['Created'],
        "author": {
          "id": message['CreatedBy'],
          "name": message['CreatedByName'],
          "profileImage": message['CreatedByAvatar']
        },
        "text": message['Text'],
        "attachment": None
    }

    if message['AttachmentUrl']:
        formatted.attachment = {
          "url": message['AttachmentUrl'],
          "name": message['AttachmentName']
        }
    return formatted
    

def formatParticipant(participant):
    formatted = {
        "id": participant['PersonId'],
        "firstName": participant['FirstName'],
        "lastName": participant['LastName'],
        "profile": participant['ProfileUrl'],
        "profileImage": participant['ProfileImageUrl']
    }
    return formatted
    