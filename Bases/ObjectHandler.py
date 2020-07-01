import pygame.sprite


class ObjectHandler:

    def __init__(self):
        """
        This is where all of our meta-level object manipulation will take place.
        """

        self.objects = pygame.sprite.Group()  # just a simple list to hold all of our objects.
        #  We can extend this to multiple lists if needed.

    def update_objects(self):
        """
        This function is a gateway function calling every object notifying of a frame update.
        :return: None
        """
        for obj in self.objects.sprites():
            obj.update(self)

    def draw_objects(self, surface):
        """
        This function is a gateway function calling every object and passing surface,
        allowing each object to handle its own drawing.
        :param surface: The pygame surface that objects will draw on.
        :return: None
        """
        for obj in self.objects.sprites():
            obj.render(surface)

    def get_objects(self):
        """
        Simply returns the list of objects.
        :return: list of all objects this object handler knows of.
        """
        return self.objects.sprites()

    def new_object(self, obj):
        """
        Add a new object in to the objects list.
        :param obj: An object that will be tracked by the ObjectHandler
        :return: None
        """
        self.objects.add(obj)

    def remove_object(self, obj):
        """
        Remove an object from the object handler sprite group effectively trashing the object.
        :param obj:
        :return:None
        """
        self.objects.remove(obj)

    def handle_input(self, events, pressed_keys):
        """
        Fires whenever an event happens through pygame.
        :param events: pygame event list
        :param pressed_keys:  long list of 0 or 1 for if a key is pressed. pygame.K_#### works in the array indexing.
        :return: None
        """
        for obj in self.objects:
            obj.handle_input(self, events, pressed_keys)

    def does_obj_exist(self, obj):
        """
        Simple check to see if an object exists according to the object handler
        :param obj:
        :return: true or false on if object exists
        """
        return self.objects.has(obj)
