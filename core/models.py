from django.db import models
from django.db.models import Avg, Max, Min, Sum, Count

class SimulationSession(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    source_path = models.CharField(max_length=500, db_index=True)
    def get_aggregated_stats(self):
        stats = self.trajectorypoint_set.aggregate(
            x_avg=Avg('pos_x'), x_sum=Sum('pos_x'), x_min=Min('pos_x'), x_max=Max('pos_x'),
            y_avg=Avg('pos_y'), y_sum=Sum('pos_y'), y_min=Min('pos_y'), y_max=Max('pos_y'),
            z_avg=Avg('pos_z'), z_sum=Sum('pos_z'), z_min=Min('pos_z'), z_max=Max('pos_z'),
            total_time=Max('sim_time'),
            total_points=Count('id')
        )
        
        # Zabezpieczenie przed pustymi sesjami
        return {k: (v if v is not None else 0.0) for k, v in stats.items()}

class TrajectoryPoint(models.Model):
    session = models.ForeignKey(SimulationSession, on_delete=models.CASCADE)
    sim_time = models.FloatField(db_index=True)
    pos_x = models.FloatField()
    pos_y = models.FloatField()
    pos_z = models.FloatField()

class ValidationError(models.Model):
    session = models.ForeignKey(SimulationSession, on_delete=models.CASCADE)
    file_name = models.CharField(max_length=255, db_index=True)
    error_details = models.TextField(db_index=True)
    raw_data = models.TextField(db_index=True)