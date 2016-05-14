## gets videos based on direction. this funciton is used in the videos class
def get_vid_for_direction(instance=None,direction=None):
    if(instance is None):
        return None
        
    current_category = instance.category
    next_vid = None
    if(direction == "next"):
        videos = current_category.video_set.all().filter(order__gt=instance.order)
    else:
        videos = current_category.video_set.all().filter(order__lt=instance.order).reverse()
    if len(videos) >=1:
            try:
                next_vid = videos[0].get_absolute_url()
            except IndexError:
                pass
    return next_vid