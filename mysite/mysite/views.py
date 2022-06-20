from django_tables2 import SingleTableView

from .models import User
from .tables import RankingTable

class RankingTableView(SingleTableView):
    model = User
    table_class = RankingTable
    template_name = 'ranking.html'