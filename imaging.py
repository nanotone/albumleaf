import PIL.Image

axes = {'width': 0, 'height': 1,
        'w': 0, 'h': 1,
        'x': 0, 'y': 1,
}

# map each EXIF orientation value to the PIL ops which produce that orientation
orientation_transforms = {
    1: (),
    2: (PIL.Image.FLIP_LEFT_RIGHT,),
    3: (PIL.Image.ROTATE_180,),
    4: (PIL.Image.FLIP_TOP_BOTTOM,),
    5: (PIL.Image.FLIP_LEFT_RIGHT, PIL.Image.ROTATE_270),
    6: (PIL.Image.ROTATE_270,),
    7: (PIL.Image.FLIP_LEFT_RIGHT, PIL.Image.ROTATE_90),
    8: (PIL.Image.ROTATE_90,),
}

def generate_sizes(path, reqs, ext):
    (prefix, orig_ext) = path.rsplit('.', 1)
    image = PIL.Image.open(path)
    try:
        orientation = image._getexif()[274]
        assert 1 <= orientation <= 8
    except (AssertionError, AttributeError, KeyError, TypeError):
        orientation = 1
    dims = image.size
    if orientation in (5, 6, 7, 8):
        dims = dims[::-1]
    sizes = []
    for req in reqs:
        scale = max(float(reqsize) / dim for (reqsize, dim) in zip(req[:2], dims))  # smallest scale that meets all requirements
        if len(req) < 3 or not req[2].get('allow_upsize', False):
            scale = min(1.0, scale)  # never upscale unless we explicitly allow it
        naive_dims = [int(round(s * scale)) for s in image.size]  # untransposed scaled dimensions
        image2 = image.resize(tuple(naive_dims), PIL.Image.ANTIALIAS)  # nicest resampling

        # transpose after resizing because it's somewhat expensive and probably lossy
        for t in orientation_transforms[orientation]:
            image2 = image2.transpose(t)

        # crop to final size now, which will make all future ops cheaper
        if len(req) > 2 and req[2].get('crop'):
            numnames = ((0, 'w'), (1, 'h'))
            # calculate upper-left corner of crop, minimum (0, 0)
            pos = [max(image2.size[i] - req[i], 0) / 2 for i in (0, 1)]
            # append lower-right corner of crop, maximum image2.size
            box = pos + [min(pos[i] + req[i], image2.size[i]) for i in (0, 1)]
            image2 = image2.crop(tuple(box))

        if image2.mode != 'RGB':
            image2 = image2.convert('RGB')
        image2.save('%s_%dx%d.%s' % (prefix, image2.size[0], image2.size[1], ext))
        sizes.append(image2.size)
    return sizes

