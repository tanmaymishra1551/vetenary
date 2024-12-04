from django.db import models

class Farmer(models.Model):
    farmer_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    contact = models.CharField(max_length=15)
    address = models.TextField()

    def __str__(self):
        return self.name

class Cattle(models.Model):
    cattle_id = models.AutoField(primary_key=True)
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE, related_name='cattle')
    name = models.CharField(max_length=100, blank=True, null=True)
    breed = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    health_status = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return f"{self.name or 'Cattle'} - {self.breed}"

class Veterinary(models.Model):
    vet_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    contact = models.CharField(max_length=15)
    specialization = models.CharField(max_length=200)
    location = models.TextField()

    def __str__(self):
        return self.name

class Appointment(models.Model):
    appointment_id = models.AutoField(primary_key=True)
    vet = models.ForeignKey(Veterinary, on_delete=models.CASCADE, related_name='appointments')
    cattle = models.ForeignKey(Cattle, on_delete=models.CASCADE, related_name='appointments')
    date = models.DateField()
    time = models.TimeField()
    purpose = models.TextField()

    def __str__(self):
        return f"Appointment with {self.vet.name} on {self.date}"

class MilkProduction(models.Model):
    record_id = models.AutoField(primary_key=True)
    cattle = models.ForeignKey(Cattle, on_delete=models.CASCADE, related_name='milk_productions')
    date = models.DateField()
    milk_yield = models.DecimalField(max_digits=5, decimal_places=2)  # in liters

    def __str__(self):
        return f"{self.cattle.name or 'Cattle'} - {self.milk_yield} L on {self.date}"

class DiseaseRecord(models.Model):
    record_id = models.AutoField(primary_key=True)
    cattle = models.ForeignKey(Cattle, on_delete=models.CASCADE, related_name='disease_records')
    disease = models.CharField(max_length=200)
    symptoms = models.TextField()
    treatment = models.TextField()

    def __str__(self):
        return f"{self.cattle.name or 'Cattle'} - {self.disease}"

class Marketplace(models.Model):
    listing_id = models.AutoField(primary_key=True)
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE, related_name='marketplace_listings')
    item_name = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.item_name} - {self.price} by {self.farmer.name}"

