from rest_framework import serializers

from LunchCloud.models import Profile, Availability, FoodOption, LunchAppointment, IntroductionCode, Location


class WhitelistSerializer(serializers.Serializer):
    id = serializers.SerializerMethodField()
    name = serializers.CharField()

    def get_id(self, obj: FoodOption):
        return obj.external_id


class ProfileSerializer(serializers.Serializer):
    email = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    locations = LocationSerializer(many=True)
    whitelist = WhitelistSerializer(many=True)

    def get_email(self, obj: Profile):
        return obj.user.email

    def get_name(self, obj: Profile):
        return "{1}, {0}".format(obj.user.first_name, obj.user.last_name)

    def get_locations(self, obj: Profile):
        return [(location.external_id, location.name) for location in obj.locations.all()]

    def get_whitelist(self, obj: Profile):
        return [(foodtype.external_id, foodtype.name) for foodtype in obj.whitelist.all()]


class AvailabilitySerializer(serializers.Serializer):
    date_str = serializers.SerializerMethodField()
    in_use = serializers.SerializerMethodField()

    def get_date_str(self, obj: Availability):
        return obj.frm.isoformat()

    def get_in_use(self, obj: Availability):
        return False


class FoodOptionSerializer(serializers.Serializer):
    id = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()

    def get_id(self, obj: FoodOption):
        return obj.external_id

    def get_name(self, obj: FoodOption):
        return obj.name


class FoodOptionAPISerializer(serializers.Serializer):
    success = serializers.BooleanField()
    message = serializers.CharField(max_length=80)
    food_options = FoodOptionSerializer(many=True)


class LocationSerializer(serializers.Serializer):
    id = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()

    def get_id(self, obj: Location):
        return obj.external_id

    def get_name(self, obj: Location):
        return obj.name


class LocationAPISerializer(serializers.Serializer):
    success = serializers.BooleanField()
    message = serializers.CharField(max_length=80)
    locations = LocationSerializer(many=True)


class ProfileAPISerializer(serializers.Serializer):
    success = serializers.BooleanField()
    updated = serializers.BooleanField()
    message = serializers.CharField(max_length=80)
    profile = ProfileSerializer()


class AvailabilityAPISerializer(serializers.Serializer):
    success = serializers.BooleanField()
    updated = serializers.BooleanField()
    message = serializers.CharField(max_length=80)
    availability = AvailabilitySerializer(many=True)


class AppointmentSerializer(serializers.Serializer):

    id = serializers.SerializerMethodField()
    date = serializers.SerializerMethodField()
    title = serializers.CharField()
    location = serializers.CharField()
    people = serializers.SerializerMethodField()
    space_available = serializers.SerializerMethodField()

    # This is not really used by us right now, but may be used to highlight lunches later.
    # On the front end it is used to highlight search results.
    highlight = serializers.BooleanField(default=False)

    def get_space_available(self, obj: LunchAppointment):
        return obj.max_attendees - obj.attendees.count()

    def get_people(self, obj: LunchAppointment):
        try:
            return [(profile.external_id, profile.user.username) for profile in obj.attendees.all()]
        except AttributeError:
            return []

    def get_id(self, obj):
        try:
            return obj.external_id
        except AttributeError:
            return self.initial_data.get('external_id')

    def get_date(self, obj):
        try:
            return obj.event_date
        except AttributeError:
            return self.initial_data.get('event_date')


class AppointmentAPISerializer(serializers.Serializer):
    success = serializers.BooleanField()
    message = serializers.CharField(max_length=80)
    appointments = AppointmentSerializer(many=True)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


class SearchAPISerializer(serializers.Serializer):
    success = serializers.BooleanField()
    message = serializers.CharField(max_length=80)
    everyone = AppointmentSerializer(many=True)
    youonly = AppointmentSerializer(many=True)


class IntroductionAPISerializer(serializers.Serializer):
    success = serializers.BooleanField()
    message = serializers.CharField(max_length=80)
    introduction_code = serializers.SerializerMethodField()

    def get_introduction_code(self, obj: IntroductionCode):
        return obj.code
