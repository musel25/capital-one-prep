"""Original constructed exercise; not employer interview material."""

SPEC = {'number': 9,
 'slug': 'iterator-batches',
 'title': 'Keep the final iterator batch',
 'difficulty': 'Easy',
 'time': 20,
 'prerequisites': 'Lists, dictionaries, and functions.',
 'learn': 'An iterator gives values one at a time and remembers its current position. You can '
          'group its values without indexing the original sequence. itertools.islice reads up to a '
          'fixed number of values from the current iterator position. The final group can be '
          'shorter than the requested batch size. That partial group still contains work and must '
          'be emitted. Stop only when a read returns no values. In a real streaming application, '
          'this pattern can limit the active buffer to one batch. This exercise returns every '
          'batch as JSON, so the complete result still occupies memory. The grouping logic should '
          'preserve every item exactly once.',
 'task': '`data` has `values`, a list of integers from -1,000,000 through 1,000,000, and `size`, '
         'an integer from 1 through 20. Return consecutive batches as a list of lists. Each batch '
         'has `size` items except a possible final nonempty partial batch. Preserve order and '
         'duplicates. An empty input returns an empty list. Use an iterator and itertools.islice '
         'for practice; the judge checks the grouping behavior.',
 'constraints': ['At most 100 input items. All input values follow the stated contract.'],
 'hints': ['Create the iterator once, outside the loop.',
           'An empty batch ends the loop; a short batch does not.'],
 'starter': 'def solve(data: dict) -> list[list[int]]:\n    raise NotImplementedError\n',
 'reference': 'from itertools import islice\n'
              '\n'
              'def solve(data: dict) -> list[list[int]]:\n'
              "    values = iter(data['values'])\n"
              '    batches = []\n'
              '    while True:\n'
              "        batch = list(islice(values, data['size']))\n"
              '        if not batch:\n'
              '            break\n'
              '        batches.append(batch)\n'
              '    return batches\n',
 'java': 'public Object solve(Map<String,Object> d) {\n'
         '    List<Object> values=arr(d.get("values")),out=new ArrayList<>(); int '
         'size=n(d.get("size"));\n'
         '    for(int i=0;i<values.size();i+=size) out.add(new '
         'ArrayList<>(values.subList(i,Math.min(values.size(),i+size))));\n'
         '    return out;\n'
         '}',
 'approach': 'The reference consumes one iterator with islice. Time is O(n). The active batch uses '
             'O(size) space, but this JSON return value stores O(n) items. The judge cannot prove '
             'iterator use or memory complexity. Production consumers can process each batch as it '
             'is produced.',
 'cases': [{'input': {'values': [1, 2, 3, 4, 5], 'size': 2},
            'expected': [[1, 2], [3, 4], [5]],
            'label': 'final partial batch'},
           {'input': {'values': [7, 8, 9, 10], 'size': 2},
            'expected': [[7, 8], [9, 10]],
            'label': 'exact multiple'},
           {'input': {'values': [], 'size': 3}, 'expected': [], 'label': 'empty iterator'},
           {'input': {'values': [1], 'size': 1},
            'expected': [[1]],
            'label': 'singleton exact batch'},
           {'input': {'values': [1], 'size': 20},
            'expected': [[1]],
            'label': 'batch larger than input'},
           {'input': {'values': [1, 2, 3], 'size': 1},
            'expected': [[1], [2], [3]],
            'label': 'size one'},
           {'input': {'values': [0, 0, 0], 'size': 2},
            'expected': [[0, 0], [0]],
            'label': 'repeated zero values'},
           {'input': {'values': [-3, -2, -1, 0], 'size': 3},
            'expected': [[-3, -2, -1], [0]],
            'label': 'negative values'},
           {'input': {'values': [1, 2, 3], 'size': 3},
            'expected': [[1, 2, 3]],
            'label': 'one full batch'},
           {'input': {'values': [], 'size': 1}, 'expected': [], 'label': 'empty size one'},
           {'input': {'values': [5, 4, 3, 2, 1, 0], 'size': 4},
            'expected': [[5, 4, 3, 2], [1, 0]],
            'label': 'partial batch with two values'},
           {'input': {'values': [1000000, -1000000], 'size': 20},
            'expected': [[1000000, -1000000]],
            'label': 'value and batch boundaries'}],
 'generated': [{'values': [0, 1, 2, 3, 4, 5, 6], 'size': 2},
               {'values': [0, 1, 2, 3, 4, 5, 6, 7], 'size': 3},
               {'values': [0, 1, 2, 3, 4, 5, 6, 7, 8], 'size': 4},
               {'values': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9], 'size': 5},
               {'values': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 'size': 6},
               {'values': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11], 'size': 2},
               {'values': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], 'size': 3},
               {'values': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13], 'size': 4},
               {'values': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14], 'size': 5},
               {'values': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15], 'size': 6},
               {'values': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16], 'size': 2},
               {'values': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17],
                'size': 3}],
 'mutations': [{'name': 'drops short final batch',
                'old': 'if not batch:',
                'new': "if len(batch) < data['size']:"}],
 'sources': ['https://docs.python.org/3.11/library/itertools.html#itertools.islice']}
