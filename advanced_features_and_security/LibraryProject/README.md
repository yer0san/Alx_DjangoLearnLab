# Django Permissions and Groups Setup

## Model Permissions

- `can_view` – Allows a user to view books.
- `can_create` – Allows a user to create new books.
- `can_edit` – Allows a user to edit existing books.
- `can_delete` – Allows a user to delete books.

These permissions are defined in the `Book` model using the `Meta` class:

```python
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    
    class Meta:
        permissions = [
            ('can_view', 'Can view book'),
            ('can_create', 'Can create book'),
            ('can_edit', 'Can edit book'),
            ('can_delete', 'Can delete book'),
        ]
```
## User Groups

- `Admins` – Full access (`can_view`, `can_create`, `can_edit`, `can_delete`)
- `Editors` – Limited access (`can_view`, `can_edit`)
- `Viewers` – Read-only access (`can_view`)

## Assigning Users to Groups



```python
from django.contrib.auth.models import User, Group

user = User.objects.get(username='john')
editors_group = Group.objects.get(name='Editors')
user.groups.add(editors_group)
