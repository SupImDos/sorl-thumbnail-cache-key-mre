# MRE of `sorl-thumbnail` v12 -> v13 cache key issue

## Steps to reproduce

1. Setup environment with `sorl-thumbnail==12.11.0`
2. Run the development server
3. Create some `ExampleModel` records in Django-admin
4. Access the example page to generate some thumbnails and cache entries
5. Stop the server and upgrade to `sorl-thumbnail==13.0.0`
6. Run the development server again
7. Access the example page again and observe that thumbnails are regenerated and cache entries are duplicated

## Results

### Storage before upgrade
```bash
$ tree storage
storage
├── files
│   └── 1a.jpg
└── thumbnails
    └── ea
        └── b5
            └── eab52556ed29cf8033e2cf8496f78e11.jpg
```

### Cache contents before upgrade
```python
# 7b3c0a79a702633cf8dac170ff7e2e77.djcache ["c5cdf2b3e220d1926fd9ef2103898002"]
# 17d6d7f3ce5a3e0fb351501076ec83ad.djcache {"name": "files/1a.jpg", "storage": "django.core.files.storage.filesystem.FileSystemStorage", "size": [200, 200]}
# 208e071ed0af786c1a70ddcd94aa23ab.djcache {"name": "thumbnails/ea/b5/eab52556ed29cf8033e2cf8496f78e11.jpg", "storage": "django.core.files.storage.filesystem.FileSystemStorage", "size": [100, 100]}
```

### Database contents before upgrade
```python
{'key': 'sorl-thumbnail||thumbnails||a65023c736963829d8ca4b19bc55dcdb', 'value': '["c5cdf2b3e220d1926fd9ef2103898002"]'}
{'key': 'sorl-thumbnail||image||a65023c736963829d8ca4b19bc55dcdb', 'value': '{"name": "files/1a.jpg", "storage": "django.core.files.storage.filesystem.FileSystemStorage", "size": [200, 200]}'}
{'key': 'sorl-thumbnail||image||c5cdf2b3e220d1926fd9ef2103898002', 'value': '{"name": "thumbnails/ea/b5/eab52556ed29cf8033e2cf8496f78e11.jpg", "storage": "django.core.files.storage.filesystem.FileSystemStorage", "size": [100, 100]}'}
```

### Storage after upgrade
```bash
$ tree storage
storage
├── files
│   └── 1a.jpg
└── thumbnails
    ├── ad
    │   └── c6
    │       └── adc63e980ad9a43688ab6639fc43a018.jpg
    └── ea
        └── b5
            └── eab52556ed29cf8033e2cf8496f78e11.jpg
```

### Cache contents after upgrade
```python
# 7b3c0a79a702633cf8dac170ff7e2e77.djcache ["c5cdf2b3e220d1926fd9ef2103898002"]
# 17d6d7f3ce5a3e0fb351501076ec83ad.djcache {"name": "files/1a.jpg", "storage": "django.core.files.storage.filesystem.FileSystemStorage", "size": [200, 200]}
# 208e071ed0af786c1a70ddcd94aa23ab.djcache {"name": "thumbnails/ea/b5/eab52556ed29cf8033e2cf8496f78e11.jpg", "storage": "django.core.files.storage.filesystem.FileSystemStorage", "size": [100, 100]}
# 7754358ea62b22c5502a60399c796b52.djcache ["1e90480789d4158e934a7d8fe3168993"]
# fc0749dbe763143f1942fcb4a99e8af3.djcache {"name": "files/1a.jpg", "storage": "default", "size": [200, 200]}
# c7fa9ce59acba7f1318c638de30b5c88.djcache {"name": "thumbnails/ad/c6/adc63e980ad9a43688ab6639fc43a018.jpg", "storage": "default", "size": [100, 100]}
```

### Database contents after upgrade
```python
{'key': 'sorl-thumbnail||thumbnails||a65023c736963829d8ca4b19bc55dcdb', 'value': '["c5cdf2b3e220d1926fd9ef2103898002"]'}
{'key': 'sorl-thumbnail||image||a65023c736963829d8ca4b19bc55dcdb', 'value': '{"name": "files/1a.jpg", "storage": "django.core.files.storage.filesystem.FileSystemStorage", "size": [200, 200]}'}
{'key': 'sorl-thumbnail||image||c5cdf2b3e220d1926fd9ef2103898002', 'value': '{"name": "thumbnails/ea/b5/eab52556ed29cf8033e2cf8496f78e11.jpg", "storage": "django.core.files.storage.filesystem.FileSystemStorage", "size": [100, 100]}'}
{'key': 'sorl-thumbnail||thumbnails||487a409c588e4af76fa3a2b204487861', 'value': '["1e90480789d4158e934a7d8fe3168993"]'}
{'key': 'sorl-thumbnail||image||487a409c588e4af76fa3a2b204487861', 'value': '{"name": "files/1a.jpg", "storage": "default", "size": [200, 200]}'}
{'key': 'sorl-thumbnail||image||1e90480789d4158e934a7d8fe3168993', 'value': '{"name": "thumbnails/ad/c6/adc63e980ad9a43688ab6639fc43a018.jpg", "storage": "default", "size": [100, 100]}'}
```
