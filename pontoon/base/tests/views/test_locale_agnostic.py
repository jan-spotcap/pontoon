import pytest

from mock import MagicMock, PropertyMock, patch

from django.http import HttpResponse
from django.urls import reverse
from django.contrib.auth.models import User


@patch('pontoon.base.views.get_object_or_404')
@patch('pontoon.base.views.utils.get_project_locale_from_request')
@patch('pontoon.base.views.Project.objects.available')
@patch('pontoon.base.views.reverse')
@patch('pontoon.base.views.redirect')
@pytest.mark.django_db
def test_view_lang_agnostic_authed(redirect_mock, reverse_mock, projects_mock,
                                   util_mock, get_mock, client):
    ''' User is authenticated and Userprofile.custom_homepage defined,
    redirect to Userprofile.custom_homepage '''
    client.force_login(User.objects.get_or_create(username='testuser')[0])

    view = reverse(
        'pontoon.translate.locale.agnostic',
        kwargs=dict(slug='FOO', part='BAR'))

    # mock return value for url reverse
    reverse_mock.return_value = 73

    # mock return value for Project.objects.available
    projects_mock.return_value = 'AVAILABLEPROJECTS'

    # create a mock Project with .locales
    project_mock = MagicMock()
    type(project_mock).locales = PropertyMock(return_value='LOCALES')

    # mock return value for get_object_or_404 for Project
    get_mock.return_value = project_mock

    # mock return value for redirect
    mock_response = HttpResponse()
    redirect_mock.return_value = mock_response

    # mock return_value for get_project_locale_from_request
    util_mock.return_value = 23

    profile_mock = MagicMock()
    type(profile_mock).custom_homepage = PropertyMock(return_value=None)

    # mock return_value for user.is_authenticated and custom homepage
    user_mock = MagicMock()
    type(user_mock).is_authenticated = PropertyMock(return_value=True)
    type(user_mock).profile = PropertyMock(return_value=profile_mock)

    response = client.get(view)

    # Project.objects.available was called with no args
    assert list(projects_mock.call_args) == [(), {}]

    # get_object_or_404 was called with Project.objects.available and
    # the requested slug
    assert (
        list(get_mock.call_args)
        == [('AVAILABLEPROJECTS',), {'slug': u'FOO'}])

    # reverse was called with args...
    assert (
        list(reverse_mock.call_args)
        == [('pontoon.translate',),
            {'kwargs': {
                'locale': 23,
                'part': u'BAR',
                'slug': u'FOO'}}])

    # redirect was called with reverse result
    assert(
        list(redirect_mock.call_args)
        == [('73',), {}])
    assert response is mock_response


@patch('pontoon.base.views.get_object_or_404')
@patch('pontoon.base.views.utils.get_project_locale_from_request')
@patch('pontoon.base.views.Project.objects.available')
@patch('pontoon.base.views.reverse')
@patch('pontoon.base.views.redirect')
def test_view_lang_agnostic_anon_available_accept_language(redirect_mock,
                                                           reverse_mock,
                                                           projects_mock,
                                                           util_mock,
                                                           get_mock, client):
    '''User is not authenticated, redirect to first
        available accept-language locale'''
    view = reverse(
        'pontoon.translate.locale.agnostic',
        kwargs=dict(slug='FOO', part='BAR'))

    # mock return value for url reverse
    reverse_mock.return_value = 73

    # mock return value for Project.objects.available
    projects_mock.return_value = 'AVAILABLEPROJECTS'

    # create a mock Project with .locales
    project_mock = MagicMock()
    type(project_mock).locales = PropertyMock(return_value='LOCALES')

    # mock return value for get_object_or_404 for Project
    get_mock.return_value = project_mock

    # mock return value for redirect
    mock_response = HttpResponse()
    redirect_mock.return_value = mock_response

    # mock return_value for get_project_locale_from_request
    util_mock.return_value = 23

    response = client.get("%s?baz=17" % view)

    # Project.objects.available was called with no args
    assert list(projects_mock.call_args) == [(), {}]

    # get_object_or_404 was called with Project.objects.available and
    # the requested slug
    assert (
        list(get_mock.call_args)
        == [('AVAILABLEPROJECTS',), {'slug': u'FOO'}])

    # get_project_locale_from_request
    assert (
        list(util_mock.call_args)
        == [(response.wsgi_request, 'LOCALES'), {}])

    # reverse was called with args...
    assert (
        list(reverse_mock.call_args)
        == [('pontoon.translate',),
            {'kwargs': {
                'locale': 23,
                'part': u'BAR',
                'slug': u'FOO'}}])

    # redirect was called with reverse result
    assert (
        list(redirect_mock.call_args)
        == [('73?baz=17',), {}])
    assert response is mock_response


@patch('pontoon.base.views.get_object_or_404')
@patch('pontoon.base.views.utils.get_project_locale_from_request')
@patch('pontoon.base.views.Project.objects.available')
@patch('pontoon.base.views.reverse')
@patch('pontoon.base.views.redirect')
def test_view_lang_agnostic_anon_unavailable_accept_language(redirect_mock,
                                                             reverse_mock,
                                                             projects_mock,
                                                             util_mock,
                                                             get_mock, client):
    ''' User is not authenticated and Userprofile.custom_homepage not defined,
    redirect to project dashboard '''

    view = reverse(
        'pontoon.translate.locale.agnostic',
        kwargs=dict(slug='FOO', part='BAR'))

    # mock return value for url reverse
    reverse_mock.return_value = 73

    # mock return value for Project.objects.available
    projects_mock.return_value = 'AVAILABLEPROJECTS'

    # create a mock Project with .locales
    project_mock = MagicMock()
    type(project_mock).locales = PropertyMock(return_value='LOCALES')

    # mock return value for get_object_or_404 for Project
    get_mock.return_value = project_mock

    # mock return value for redirect
    mock_response = HttpResponse()
    redirect_mock.return_value = mock_response

    # mock return_value for get_project_locale_from_request
    util_mock.return_value = None

    response = client.get("%s?foo=bar" % view)

    # Project.objects.available was called with no args
    assert list(projects_mock.call_args) == [(), {}]

    # get_object_or_404 was called with Project.objects.available and
    # the requested slug
    assert (
        list(get_mock.call_args)
        == [('AVAILABLEPROJECTS',), {'slug': u'FOO'}])

    # get_project_locale_from_request
    assert (
        list(util_mock.call_args)
        == [(response.wsgi_request, 'LOCALES'), {}])

    # reverse was called with args...
    assert (
        list(reverse_mock.call_args)
        == [('pontoon.projects.project',),
            {'kwargs': {'slug': u'FOO'}}])

    # redirect was called with reverse result
    assert (
        list(redirect_mock.call_args)
        == [('73?foo=bar',), {}])

    assert response is mock_response
