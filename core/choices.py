from django.utils.translation import gettext_lazy as _

YEARS = (
    (1, "1"),
    (2, "2"),
    (3, "3"),
    (4, "4"),
    (4, "5"),
    (4, "6"),
)

BACHELOR_DEGREE = "Bachelor"
MASTER_DEGREE = "Master"

LEVEL = (
    (BACHELOR_DEGREE, _("Bachelor Degree")),
    (MASTER_DEGREE, _("Master Degree")),
)

BACHLOAR_DEGREE = "Bachloar"
RESULT_LEVEL = (
    (BACHLOAR_DEGREE, "Bachloar Degree"),
    (MASTER_DEGREE, "Master Degree"),
)

FIRST = "First"
SECOND = "Second"
THIRD = "Third"

SEMESTER = (
    (FIRST, _("First")),
    (SECOND, _("Second")),
    (THIRD, _("Third")),
)
