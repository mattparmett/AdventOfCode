INPUT = 'input.txt'

class TransformationMap:
    def __init__(self, source_start, dest_start, length):
        self.source_start = source_start
        self.dest_start = dest_start
        self.length = length
        self.source_end = source_start + length

    def includes_source(self, n):
        return n in range(
            self.source_start,
            self.source_start + self.length + 1
        )

    def map_source_to_dest(self, source):
        if self.includes_source(source):
            return source - self.source_start + self.dest_start
        return source


class Transformation:
    def __init__(self, map_input):
        # map_input should be a section of the input file
        # corresponding to one set of transformation ranges
        self.name = ""
        self.transformation_maps = []

        lines = map_input.split('\n')
        for line in lines:
            if not line:
                continue

            if not line[0].isdigit():
                self.name = line.split()[0]
                continue

            tokens = [int(t) for t in line.split()]
            dest_start = tokens[0]
            source_start = tokens[1]
            length = tokens[2]

            transform_map = TransformationMap(source_start, dest_start, length)
            self.transformation_maps.append(transform_map)

    def transform_seed(self, source):
        for transform_map in self.transformation_maps:
            if transform_map.includes_source(source):
                return transform_map.map_source_to_dest(source)
        return source

    def _process_range(self, range_, transform_map):
        """
        Finds three ranges:
            1. Source range overhang before given transformation map
            2. Source range overhang after given transformation map
            3. Overlap of source range & transformation map

        For #3, we can transform the source range into dest directly
        via the transformation map.

        For #1 and #2, we return those ranges to the caller, indicating
        they still need to be processed because the given transformation
        map does not have maps for the source values.
        """

        add_to_next_range_lst = []
        add_to_result = []

        range_start, range_end = range_

        before_transform_map = (
            range_start,
            min(range_end, transform_map.source_start)
        )

        after_transform_map = (
            max(range_start, transform_map.source_end),
            range_end
        )

        transform_map_range_overlap = (
            # The number we didn't choose for the end of prior
            max(range_start, transform_map.source_start),

            # The number we didn't choose for the start of after
            min(transform_map.source_end, range_end)
        )

        # If parts of the range extend before/after the transform
        # map, we still have to process them.  Add them to the range
        # list that we will pass back to the caller, telling the caller
        # to re-analyze those ranges.

        if before_transform_map[1] > before_transform_map[0]:
            add_to_next_range_lst.append(before_transform_map)

        if after_transform_map[1] > after_transform_map[0]:
            add_to_next_range_lst.append(after_transform_map)

        # If there was overlap between source range and transform map,
        # transform that portion of the source map and return it to caller
        # telling the caller to add it to the result.

        if transform_map_range_overlap[1] > transform_map_range_overlap[0]:
            transformed_range = tuple([
                n - transform_map.source_start + transform_map.dest_start
                for n in transform_map_range_overlap
            ])

            add_to_result.append(transformed_range)

        return add_to_next_range_lst, add_to_result


    def transform_range(self, source_range):
        range_lst = source_range
        result = []
        for transform_map in self.transformation_maps:
            next_range_lst = []
            while range_lst:
                range_ = range_lst.pop()
                add_to_next, add_to_result = self._process_range(range_, transform_map)
                next_range_lst.extend(add_to_next)
                result.extend(add_to_result)

            range_lst = next_range_lst
        
        result.extend(range_lst)
        return result


class Pipeline:
    def __init__(self, transformations):
        self.transformations = transformations

    def apply(self, seed):
        dest = seed
        for transformation in self.transformations:
            dest = transformation.transform_seed(dest)
        return dest

    def apply_range(self, seed_range):
        dest_range = [seed_range]
        for transformation in self.transformations:
            dest_range = transformation.transform_range(dest_range)
        return dest_range


def parse_input():
    """
    Returns (
        array of seeds for p1,
        array of seed ranges for p2,
        array of transformations
    )

    Note that seed ranges for p2 are inclusive
    of the start element, but exclusive of the
    end element (because we calculate end as start + len).
    """

    lines = []
    with open(INPUT) as f:
        contents = f.read()

    sections = contents.split('\n\n')
    
    seeds_p1 = [int(t) for t in sections[0].split(':')[1].split()]


    p2_seed_range_inputs = list(zip(seeds_p1[::2], seeds_p1[1::2]))  # seed[0], seed[1] both jumping by 2
    seeds_p2 = [
        (start, start + length)
        for start, length
        in p2_seed_range_inputs
    ]

    transformations = [
        Transformation(section)
        for section in sections[1:]
    ]

    pipeline = Pipeline(transformations)

    return seeds_p1, seeds_p2, pipeline


if __name__ == "__main__":
    seeds_p1, seeds_p2, pipeline = parse_input()

    min_loc_p1 = min([pipeline.apply(seed) for seed in seeds_p1])
    print(min_loc_p1)

    p2 = []
    for seed_range in seeds_p2:
        dest_range = seed_range
        dest_range = pipeline.apply_range(dest_range)
        p2.append(min(dest_range)[0])  # append the start of the smallest loc range
    print(min(p2))



