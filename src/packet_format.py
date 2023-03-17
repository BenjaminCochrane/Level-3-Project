'''Structure representing expected format'''

class PacketFormat():
    '''Structure representing the desired packet format from serial'''
    __slots__ = ['node_id',
                 'reference',
                 'rssi',
                 'frequency',
                 'transmitter_power',
                 'time'
        ]
    delineator = '_'

    def __str__(self):
        '''Return string representation'''
        return str(self.__slots__)

    def get_delineator(self):
        '''Return delineating character'''
        return self.delineator
