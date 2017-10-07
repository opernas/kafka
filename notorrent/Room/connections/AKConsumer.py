from threading import Thread
from kafka import KafkaConsumer,TopicPartition


class AKConsumer(Thread):
    def __init__(self, brokerconf, userconf):
        self.stopConsuming = False
        self.brokerconf = brokerconf
        self.userconf = userconf
        self.callback=None
        self.topic_partitions = None
        self.consumer = KafkaConsumer(**self.brokerconf)
        Thread.__init__(self)
        self._init()

    def _init(self):
        self.topic_partitions = [TopicPartition(self.userconf['topics'][0], self.userconf['partition'][0])]
        self.consumer.assign(self.topic_partitions)
        partitions = self.consumer.partitions_for_topic(self.userconf['topics'][0])
        if self.userconf['partition'][0] in partitions:
            self._user_wants_old_messages(self.topic_partitions[0])

    def _user_wants_old_messages(self, tp):
        current_offset = self.consumer.position(tp)
        user_shift_offset = self.userconf.get('resendnumber', 0)
        if user_shift_offset > 0: user_shift_offset -= 1
        self.consumer.seek(tp, current_offset - user_shift_offset)
        print(' User selected to go from ', current_offset, ' to offset ', current_offset - user_shift_offset)

    def subscribe(self,callback):
        self.callback = callback

    def run(self):
        self.stopConsuming = False
        print('Consuming thread from ', self.userconf['topics'], ' in partition ', self.userconf['partition'], ' in.')
        while not self.stopConsuming:
            msg = self.consumer.poll(300,1)
            if msg:
                self._receive(msg)
                self.consumer.commit()
        print('Consuming thread from ', self.userconf['topics'], ' in partition ', self.userconf['partition'], ' out.')

    def _receive(self,msg):
        self.callback(msg)

    def stop(self):
        self.stopConsuming = True
        self.join()
        self.consumer.close()
        print('Consumer to ', self.userconf['topics'], ' in partition ', self.userconf['partition'], ' stopped.')
