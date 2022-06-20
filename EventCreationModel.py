from telegram import User, File, Location


class EventCreationModel:   
    user: User
    event_photo: File
    user_location: Location
    CreationDate: str
    EndDate: str
    EventName: str
    EventDescription: str
