
def get_category_id(category):
    categories = {'fantasy': 46,
                  'love': 2487,
                  'children': 1415,
                  'poetry': 13,
                  'sf': 36,
                  'detective': 1123,
                  'adventure': 2849,
                  'comedies': 776
                  };
    return categories[category]

def get_category_for_id(category_id):
    categories = {46: 'fantasy',
                  2487: 'love',
                  1415: 'children',
                  13: 'poetry',
                  36: 'sf',
                  1123: 'detective',
                  2849: 'adventure',
                  776: 'comedies'
                  };
    return categories[category_id]


