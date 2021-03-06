# conftest.py

import io

import pytest

import concepts


@pytest.fixture(scope='session')
def source():
    return concepts.EXAMPLE


@pytest.fixture(scope='session')
def context(source):
    return concepts.make_context(source)


@pytest.fixture(scope='module')
def lattice(context):
    context = concepts.Context(context.objects, context.properties,
                               context.bools)
    return context.lattice


@pytest.fixture(params=['str', 'bytes', 'pathlike', 'fileobj'])
def path_or_fileobj(request, tmp_path, filename='context.json'):
    if request.param == 'str':
        yield str(tmp_path / filename)
    elif request.param == 'bytes':
        yield str(tmp_path / filename).encode('ascii')
    elif request.param == 'pathlike':
        yield tmp_path / filename
    elif request.param == 'fileobj':
        with io.StringIO() as f:
            yield f
    else:
        raise RuntimeError


@pytest.fixture(params=['utf-8', None])
def encoding(request):
    return request.param
