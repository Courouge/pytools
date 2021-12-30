from collections import deque
from names_generator import generate_name
import random

class TopicsPartitions:
    def __init__(self, topic, partition, leader, replicas, size):
        self.topic = topic
        self.partition = partition
        self.leader = leader
        self.replicas = replicas
        self.size = size
    def __str__(self):
        return ("Topic: " + str(self.topic) + ", " +
                "Partition: " + str(self.partition) + ", " +
                "Leader: " + str(self.leader) + ", " +
                "Replicas: " + str(self.replicas) + ", " +
                "Size: " + str(self.size) + " ")
################ Configuration ################
nb_of_topics = 10
broker_nodes = ["1", "2", "3"]
min_size_partition = 10000
max_size_partition = 1000000
min_partition = 1
max_partition = 5
################ Configuration ################

TopicsPartitionsMetadata = []
node_rotation = deque(broker_nodes)
for topic in [generate_name() for x in range(nb_of_topics)]:
    partitions = random.randint(min_partition, max_partition)
    size = random.randint(min_size_partition, max_size_partition)
    for partition in range(partitions):
        node_rotation.rotate(1)
        leader = list(node_rotation)[0]
        replicas = list(node_rotation)
        TopicsPartitionsMetadata.append(TopicsPartitions(topic, partition, leader, replicas, size))

# exemple of output
# Topic: awesome_chatelet, Partition: 0, Leader: 1, Replicas: ['1', '2', '3'], Size: 564806
print('\n'.join("%s" % tp for tp in TopicsPartitionsMetadata))
#newlist = sorted(ut, key=lambda x: x.count, reverse=True)
