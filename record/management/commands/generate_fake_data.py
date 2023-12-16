import random
from faker import Faker
from django.core.management.base import BaseCommand
from account.models import User, Profile
from record.models import MedicalData

fake = Faker()


class Command(BaseCommand):
    help = 'Generate and insert fake data into the database'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Populating database with fake data...'))

        # Create users and profiles
        for _ in range(10):  # Adjust the number of users you want to create
            user = User.objects.create_user(
                email=fake.email(),
                password='password123',  # Set a default password
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                is_active=True,
                is_patient=True,
            )

            Profile.objects.create(
                user=user,
                phone_number=fake.phone_number(),
                address=fake.address(),
            )


        # Create medical data
        for profile in Profile.objects.all():
            MedicalData.objects.create(
                profile=profile,
                dob=fake.date_of_birth(),
                bmi=random.randint(18, 30),
                blood_group=fake.random_element(elements=('A', 'B', 'AB', 'O')),
                allergy=fake.random_element(elements=('Pollen',
                    'Dust mites',
                    'Pet dander',
                    'Insect stings',
                    'Mold',
                    'Food (e.g., nuts, shellfish)',
                    'Latex',
                    'Medications (e.g., penicillin)',)),
                medication=fake.random_element(elements=(
                    'Aspirin',
                    'Ibuprofen',
                    'Acetaminophen',
                    'Lisinopril',
                    'Metformin',
                    'Levothyroxine',
                    'Simvastatin',
                    'Atorvastatin',
                    'Amoxicillin',
                    'Omeprazole',
                    'Albuterol',
                    'Hydrochlorothiazide',
                    'Losartan',
                    'Gabapentin',
                    'Sertraline',
                    'Metoprolol',
                    'Amlodipine',
                    'Prednisone',
                    'Citalopram',
                )),
                diagnosis=fake.random_element(elements=('Common Cold',
                            'Influenza (Flu)',
                            'Hypertension',
                            'Diabetes',
                            'Asthma',
                            'Arthritis',
                            'Heart Disease',
                            'Allergies',
                            'Migraine',
                            'Chronic Obstructive Pulmonary Disease (COPD)',
                            )
                            ),
                                    )

        self.stdout.write(self.style.SUCCESS('Fake data generation complete.'))
