from django.db import models

class SimulationSession(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    source_path = models.CharField(max_length=500, db_index=True)

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