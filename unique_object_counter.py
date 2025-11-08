from collections import defaultdict

class UniqueObjectCounter:
    def __init__(self):
        """
        Initializes the UniqueObjectCounter.
        """
        pass

    def count_unique_objects(self, detections_by_room):
        """
        Counts unique objects per room, deduplicating within each room.

        Args:
            detections_by_room (dict): A dictionary where keys are room IDs and values are lists of detections.
                                       Each detection is expected to be a dictionary with at least a 'class_name' key.

        Returns:
            dict: A dictionary where keys are room IDs and values are dictionaries of unique object counts.
                  Example: {'Room A': {'Sofa': 1, 'Chair': 1, 'TV': 1}, 'Room B': {'TV': 1}}
        """
        unique_counts_by_room = {}

        for room_id, detections in detections_by_room.items():
            unique_objects_in_room = set()
            for det in detections:
                unique_objects_in_room.add(det['class_name'])

            # Count occurrences of each unique object
            object_counts = defaultdict(int)
            for obj_name in unique_objects_in_room:
                object_counts[obj_name] = 1 # Since we only count unique, each present object gets a count of 1

            unique_counts_by_room[room_id] = dict(object_counts)

        return unique_counts_by_room

if __name__ == '__main__':
    # Example Usage
    counter = UniqueObjectCounter()

    # Scenario 1: Living room with 2 sofas, 3 chairs, 2 TVs
    detections_room_a = [
        {"class_name": "Sofa", "confidence": 0.9},
        {"class_name": "Sofa", "confidence": 0.8},
        {"class_name": "Chair", "confidence": 0.95},
        {"class_name": "Chair", "confidence": 0.85},
        {"class_name": "Chair", "confidence": 0.75},
        {"class_name": "TV", "confidence": 0.92},
        {"class_name": "TV", "confidence": 0.88},
    ]

    # Scenario 2: Apartment with 2 rooms = Room A (2 TVs), Room B (1 TV)
    detections_room_b = [
        {"class_name": "TV", "confidence": 0.91},
    ]

    detections_by_room_scenario_2 = {
        "Room A": detections_room_a, # Using detections from scenario 1 for Room A
        "Room B": detections_room_b
    }

    unique_counts_scenario_2 = counter.count_unique_objects(detections_by_room_scenario_2)
    print("Scenario 2 Output:", unique_counts_scenario_2)

    # Scenario 3: Studio room with bed + chair + duplicate bed annotation error
    detections_room_c = [
        {"class_name": "Bed", "confidence": 0.99},
        {"class_name": "Chair", "confidence": 0.80},
        {"class_name": "Bed", "confidence": 0.70}, # Duplicate bed
    ]
    detections_by_room_scenario_3 = {"Room C": detections_room_c}
    unique_counts_scenario_3 = counter.count_unique_objects(detections_by_room_scenario_3)
    print("Scenario 3 Output:", unique_counts_scenario_3)
