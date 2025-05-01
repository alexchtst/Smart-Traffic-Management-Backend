from models import Region, GuardPost, db

region_data = [
    {
        'name': 'BUNDARAN HI',
        'lat': -6.195038424697565,
        'long': 106.82294134838708
    },
    {
        'name': 'TUGU YOGYAKARTA',
        'lat': -7.782996202249882,
        'long': 110.3670435079401
    },
]

guardpost_data = [
    # BUNDARAN HI
    [
        {'name': 'gp hi 1', 'lat': -6.194330378179993, 'long': 106.82099045662729},
        {'name': 'gp hi 2', 'lat': -6.197070829927197, 'long': 106.82306892685925},
        {'name': 'gp hi 3', 'lat': -6.196440673833425, 'long': 106.82454301922235},
        {'name': 'gp hi 4', 'lat': -6.195370872230249, 'long': 106.82872944153353},
    ],
    # TUGU YOGYAKARTA
    [
        {'name': 'gp ty 1', 'lat': -7.781507999243927, 'long': 110.36720444048532},
        {'name': 'gp ty 2', 'lat': -7.782858012193257, 'long': 110.36339570358165},
        {'name': 'gp ty 3', 'lat': -7.785132827327461, 'long': 110.36673237168598},
        {'name': 'gp ty 4', 'lat': -7.782868642199235, 'long': 110.37009049746305},
    ],
]

def Seedregion(app):
    with app.app_context():
        GuardPost.query.delete()
        Region.query.delete()

        for data in region_data:
            region = Region(
                name=data['name'],
                lat=data['lat'],
                long=data['long'],
            )
            db.session.add(region)

        db.session.commit()

def Seedguardpost(app):
    with app.app_context():
        Seedregion(app)

        all_regions = Region.query.order_by(Region.id).all()

        for region, guardposts in zip(all_regions, guardpost_data):
            for guard in guardposts:
                guardpost = GuardPost(
                    name=guard['name'],
                    lat=guard['lat'],
                    long=guard['long'],
                    region_id=region.id,
                )
                db.session.add(guardpost)

        db.session.commit()
