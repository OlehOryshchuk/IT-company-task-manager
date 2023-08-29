from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse_lazy, reverse
from datetime import datetime

from ..models import Position, Team
from task_manager.models import Project

POSITION_LIST = reverse_lazy("team_manager:position-list")

WORKER_LIST = reverse_lazy("team_manager:worker-list")
CREATE_WORKER = reverse_lazy("team_manager:worker-create")

TEAM_LIST = reverse_lazy("team_manager:team-list")
CREATE_TEAM = reverse_lazy("team_manager:team-create")


class PublicPositionTest(TestCase):
    def test_position_login_required(self):
        response = self.client.get(POSITION_LIST)

        self.assertNotEqual(response.status_code, 200)


class PrivatePositionTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()

        self.user = get_user_model().objects.create_user(
            username="test_username", password="test_1234"
        )
        self.client.force_login(self.user)

        self.is_paginated_by = 5

    def test_receive_list_of_position(self):
        for i in range(10):
            Position.objects.create(
                name=f"TestName{i}"
            )

        response = self.client.get(POSITION_LIST)
        positions = Position.objects.all()[:self.is_paginated_by]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["position_list"]),
            list(positions)
        )
        self.assertTemplateUsed(response, "team_manager/position_list.html")

    def test_receive_positions_by_search_bar(self):
        Position.objects.create(name="Position1")
        Position.objects.create(name="Position2")
        searched = Position.objects.create(name="Position3")

        response = self.client.get(POSITION_LIST, data={
            "name": searched.name
        })

        self.assertEqual(response.status_code, 200)
        position_list = response.context["position_list"]
        self.assertEqual(len(position_list), 1)
        self.assertEqual(
            position_list[0].name,
            searched.name
        )


class PublicWorkerTest(TestCase):

    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="admin",
            password="admin123"
        )

    def test_worker_list_login_required(self):

        response = self.client.get(WORKER_LIST)

        self.assertNotEqual(response.status_code, 200)
        self.assertRedirects(response, "/accounts/login/?next=/workers/")

    def test_worker_detail_page_login_required(self):
        url = reverse("team_manager:worker-detail", args=[self.user.id])

        response = self.client.get(url)

        self.assertNotEqual(response.status_code, 200)
        self.assertRedirects(response, "/accounts/login/?next=/worker/1/detail/")

    def test_worker_create_page_login_required(self):
        url = reverse("team_manager:worker-create")

        response = self.client.get(url)

        self.assertNotEqual(response.status_code, 200)
        self.assertRedirects(response, "/accounts/login/?next=/worker/create/")


class PrivateWorkerTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()

        self.position = Position.objects.create(name="position")

        self.user = get_user_model().objects.create_user(
            username="test_username", password="test_1234", position=self.position
        )
        self.client.force_login(self.user)

        self.is_paginated_by = 5

    def test_receive_list_of_workers(self):
        for i in range(10):
            get_user_model().objects.create(
                username=f"worker{i}",
                password=f"worker123{i}",
                position=Position.objects.create(
                    name=f"Position{i}"
                )
            )

        response = self.client.get(WORKER_LIST)
        workers = get_user_model().objects.all()[:self.is_paginated_by]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["worker_list"]),
            list(workers)
        )
        self.assertTemplateUsed(response, "team_manager/worker_list.html")

    def test_receive_worker_by_username(self):
        get_user_model().objects.create(
            username="user1",
            password="user10987"
        )
        get_user_model().objects.create(
            username="user2",
            password="user20987"
        )

        response = self.client.get(WORKER_LIST, data={
            "username": "user2"
        })

        self.assertEqual(response.status_code, 200)
        worker_list = response.context["worker_list"]
        self.assertEqual(len(worker_list), 1)
        self.assertEqual(
            worker_list[0].username,
            "user2"
        )

    def test_display_all_workers_from_the_team(self):
        searched_worker = Team.objects.create(
            name="Team1",
            owner=self.user,
        )
        searched_worker.members.add(self.user.id)
        Team.objects.create(
            name="Team2",
            owner=self.user
        )

        response = self.client.get(WORKER_LIST, data={
            "team_members": searched_worker.id
        })

        self.assertEqual(response.status_code, 200)
        worker_list = response.context["worker_list"]
        self.assertEqual(len(worker_list), 1)
        self.assertEqual(
            worker_list[0].username,
            self.user.username
        )

    def test_view_own_detail_page_with_update_delete_actions(self):
        url = reverse("team_manager:worker-detail", args=[self.user.id])

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

        self.assertContains(response, reverse("team_manager:worker-update", args=[self.user.id]))
        self.assertContains(response, reverse("team_manager:worker-delete", args=[self.user.id]))

    def test_view_other_workers_detail_page_with_no_update_delete_actions(self):
        other_worker = get_user_model().objects.create_user(
            username="other", password="other123", position=self.position
        )
        url = reverse("team_manager:worker-detail", args=[other_worker.id])

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

        self.assertNotContains(response, reverse("team_manager:worker-update", args=[other_worker.id]))
        self.assertNotContains(response, reverse("team_manager:worker-delete", args=[other_worker.id]))

    def test_create_worker(self):
        position = Position.objects.create(name="UniquePosition")

        form_data = {
            "username": "UniqueUsername",
            "password1": "test_1234",
            "password2": "test_1234",
            "position": position.id,
            "first_name": "TestName",
            "last_name": "TestLastName",
        }

        response = self.client.post(CREATE_WORKER, data=form_data)
        self.assertRedirects(
            response,
            reverse("team_manager:worker-list"),
            target_status_code=200,
            status_code=302
        )
        self.assertTrue(get_user_model().objects.last().username == form_data["username"])


class PublicTeamTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="admin",
            password="admin123"
        )

    def test_team_list_page_login_required(self):

        response = self.client.get(TEAM_LIST)

        self.assertNotEqual(response.status_code, 200)
        self.assertRedirects(response, "/accounts/login/?next=/teams/")

    def test_team_detail_page_login_required(self):
        new_team = Team.objects.create(
            name="testteam",
            owner=self.user,
        )
        new_team.members.add(self.user)
        url = reverse("team_manager:team-detail", args=[new_team.id])

        response = self.client.get(url)

        self.assertNotEqual(response.status_code, 200)
        self.assertRedirects(response, "/accounts/login/?next=/team/1/detail/")

    def test_team_create_page_login_required(self):
        url = reverse("team_manager:team-create")

        response = self.client.get(url)

        self.assertNotEqual(response.status_code, 200)
        self.assertRedirects(response, "/accounts/login/?next=/team/create/")


class PrivateTeamTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()

        self.position = Position.objects.create(name="position")

        self.user = get_user_model().objects.create_user(
            username="test_username", password="test_1234", position=self.position
        )
        self.client.force_login(self.user)

        self.team = Team.objects.create(
            name="TestTeam",
            owner=self.user
        )

        self.is_paginated_by = 5

    def test_receive_list_of_teams(self):
        for i in range(10):
            Team.objects.create(
                name=f"team{i}",
                owner=self.user
            )

        response = self.client.get(TEAM_LIST)
        teams = Team.objects.all()[:self.is_paginated_by]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["team_list"]),
            list(teams)
        )
        self.assertTemplateUsed(response, "team_manager/team_list.html")

    def test_receive_list_of_teams_by_team_member(self):
        team_member1 = get_user_model().objects.create(
            username="user1",
            password="user123",
            position=self.position
        )
        team_member2 = get_user_model().objects.create(
            username="user2",
            password="user1234",
            position=self.position
        )
        team1 = Team.objects.create(
            name="team1",
            owner=self.user
        )
        team2 = Team.objects.create(
            name="team2",
            owner=self.user
        )
        team1.members.add(team_member1)
        team2.members.add(team_member2)

        response = self.client.get(TEAM_LIST, data={
            "members": team_member1.id
        })

        self.assertEqual(response.status_code, 200)
        team_list = response.context["team_list"]
        self.assertEqual(len(team_list), 1)
        self.assertEqual(
            team_list[0].name,
            team1.name
        )

    def test_receive_list_of_teams_that_are_working_on_project(self):
        project1 = Project.objects.create(
            name="project1",
            owner=self.user,
            deadline=datetime.today().date()
        )

        for i in range(1, 11):
            new_team = Team.objects.create(
                name=f"team{i}",
                owner=self.user
            )
            if i % 2 == 0:
                project1.teams.add(new_team.id)

        response = self.client.get(TEAM_LIST, data={
            "project": project1.id
        })

        self.assertEqual(response.status_code, 200)
        team_list = response.context["team_list"]
        self.assertEqual(len(team_list), 5)
        self.assertEqual(
            team_list[0].projects.first().name,
            project1.name
        )

    def test_view_own_team_page_with_update_delete_actions(self):
        url = reverse("team_manager:team-detail", args=[self.team.id])

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

        self.assertContains(response, reverse("team_manager:team-update", args=[self.team.id]))
        self.assertContains(response, reverse("team_manager:team-delete", args=[self.team.id]))

    def test_view_other_team_page_with_no_update_delete_actions(self):
        new_user = get_user_model().objects.create(
            username="NewUser",
            password="NewUser123",
            position=self.position
        )
        new_team = Team.objects.create(
            name="NewTeam",
            owner=new_user
        )
        url = reverse("team_manager:team-detail", args=[new_team.id])

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

        self.assertNotContains(response, reverse("team_manager:team-update", args=[self.team.id]))
        self.assertNotContains(response, reverse("team_manager:team-delete", args=[self.team.id]))
