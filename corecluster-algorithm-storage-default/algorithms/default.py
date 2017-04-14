"""
Copyright (C) 2014-2017 cloudover.io ltd.
This file is part of the CloudOver.org project

Licensee holding a valid commercial license for this software may
use it in accordance with the terms of the license agreement
between cloudover.io ltd. and the licensee.

Alternatively you may use this software under following terms of
GNU Affero GPL v3 license:

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version. For details contact
with the cloudover.io company: https://cloudover.io/


This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.


You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""


from corecluster.models.core.storage import Storage
from corecluster.utils.exception import CoreException


def select(size):
    """
    Returns the Storage which is less used and could handle image with given size
    If no storage is found, then exception "storage_not_found" is raised
    """
    storages = Storage.objects.filter(state__exact='ok')

    if storages.count() == 0:
        raise CoreException('storage_not_available')

    # order storages by free_space, which is a property method, not a field
    # storages.sort(key=lambda storage: storage.free_space)
    sorted(storages, key=lambda storage: storage.free_space)

    for storage in storages:
        if storage.free_space >= size/1024/1024:
            return storage

    raise CoreException('storage_not_available')