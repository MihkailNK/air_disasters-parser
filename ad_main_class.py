import datetime


# Class to collect information for a single disaster entry
class Disaster(object):
    __slots__ = ['disaster_id', 'date', 'vict_onland', 'passengers', 'personal', 'total', 'simple']

    def __init__(self):
        super(Disaster, self).__setattr__('disaster_id', 0)  # Disaster.disaster_id  (id in database)
        super(Disaster, self).__setattr__('date', {'y': 0, 'm': 0, 'd': 0})  # Disaster.date (date of disaster)
        super(Disaster, self).__setattr__('vict_onland', 0)  # Disaster.vict_onland  (count of victims on land)
        super(Disaster, self).__setattr__('passengers', {'onboard': -1, 'vict': -1})
        super(Disaster, self).__setattr__('personal', {'onboard': -1, 'vict': -1})
        super(Disaster, self).__setattr__('total', 0)  # Disaster.total (total count of victims)
        super(Disaster, self).__setattr__('simple', {})  # simple view of data

    def __setattr__(self, key, value):
        # Rules of setting Disaster.date
        if key is 'date':
            if type(value) is tuple:
                assert len(value) == 3, ValueError(value)
                super(Disaster, self).__setattr__('date', dict(y=value[0], m=value[1], d=value[2]))
            elif type(key) is int:
                super(Disaster, self).__setattr__('date', dict(y=value, m=self.date['m'], d=self.date['d']))
            elif type(value) is dict:
                assert (('y' and 'm' and 'd') in value.keys()) and (len(value.keys()) == 3), ValueError(value)
                self.date.update(value)

        # Rules of setting self.personal and self.passengers
        elif key in ('personal', 'passengers'):
            if type(value) is tuple:
                assert len(value) == 2, ValueError(value)
                if False in map(self.try_int, value):
                    onboard = value[0]
                    vict = value[1]
                else:
                    vict, onboard = min(value), max(value)
                super(Disaster, self).__setattr__(key, dict(onboard=onboard, vict=vict))
            elif type(value) is dict:
                dv = {}
                if ('vict' and 'onboard') in value.keys():
                    dv.update(value)
                elif (('v_passengers' and 'passengers') in value.keys()) and (key is 'passengers'):
                    dv = dict(onboard=value['passengers'], vict=value['v_passengers'])
                elif (('v_personal' and 'personal') in value.keys()) and (key is 'personal'):
                    dv = dict(onboard=value['personal'], vict=value['v_personal'])
                else:
                    assert KeyError(value)
                super(Disaster, self).__setattr__(key, dv)

        # Rules of setting Disaster.vict_onland and Disaster.disaster_id
        elif key in ('vict_onland', 'disaster_id'):
            assert type(value) in (int, str), ValueError(value)
            if self.try_int(value):
                value = int(value)
            super(Disaster, self).__setattr__(key, value)

        # Rules of setting Disaster.total
        elif key is 'total':
            check_value = 0
            if self.try_int(self.passengers['vict']):
                check_value += int(self.passengers['vict'])
            if self.try_int(self.personal['vict']):
                check_value += int(self.personal['vict'])
            if self.try_int(self.vict_onland):
                check_value += int(self.vict_onland)
            if self.try_int(value):
                value = int(value)
                if value < check_value:
                    super(Disaster, self).__setattr__(key, check_value)
                else:
                    super(Disaster, self).__setattr__(key, value)
            else:
                if check_value > 0:
                    super(Disaster, self).__setattr__(key, check_value)
                else:
                    super(Disaster, self).__setattr__(key, "No data")
        else:
            assert AttributeError(key)

    def __getattribute__(self, key):
        if key is 'simple':
            return {'id': self.disaster_id,
                    'personal': self.personal['onboard'],
                    'v_personal': self.personal['vict'],
                    'passengers': self.passengers['onboard'],
                    'v_passengers': self.passengers['vict'],
                    'v_onland': self.vict_onland,
                    'v_total': self.total,
                    'date': self.__datetime()}
        else:
            return super(Disaster, self).__getattribute__(key)
        pass

    def __text_date(self):
        if self.date['m'] > 9:
            return '{y}-{m}-{d}'.format(**self.date)
        return '{y}-0{m}-{d}'.format(**self.date)
    def __datetime(self):
        try:
            return datetime.date(int(self.date['y']), int(self.date['m']), int(self.date['d']))
        except:
            return datetime(int(self.date['y']), 0, 0)
    def __str__(self):
        return str(self.simple)

    # Function to try to convert a string to an integer
    def try_int(self, value):
        if type(value) is str:
            try:
                int(value)
                return True
            except ValueError:
                return False
        # elif type(value) in (tuple, list):
        #     for i in range(len(value)):
        #         if self.try_int(value[i]):
        #             return i
        #     return False
        else:
            assert ValueError(value)