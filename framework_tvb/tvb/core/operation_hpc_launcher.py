# -*- coding: utf-8 -*-
#
#
# TheVirtualBrain-Framework Package. This package holds all Data Management, and
# Web-UI helpful to run brain-simulations. To use it, you also need do download
# TheVirtualBrain-Scientific Package (for simulators). See content of the
# documentation-folder for more details. See also http://www.thevirtualbrain.org
#
# (c) 2012-2020, Baycrest Centre for Geriatric Care ("Baycrest") and others
#
# This program is free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software Foundation,
# either version 3 of the License, or (at your option) any later version.
# This program is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
# PARTICULAR PURPOSE.  See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with this
# program.  If not, see <http://www.gnu.org/licenses/>.
#
#
#   CITATION:
# When using The Virtual Brain for scientific publications, please cite it as follows:
#
#   Paula Sanz Leon, Stuart A. Knock, M. Marmaduke Woodman, Lia Domide,
#   Jochen Mersmann, Anthony R. McIntosh, Viktor Jirsa (2013)
#       The Virtual Brain: a simulator of primate brain network dynamics.
#   Frontiers in Neuroinformatics (7:10. doi: 10.3389/fninf.2013.00010)
#
#

import sys
from tvb.adapters.simulator.simulator_adapter import SimulatorAdapter
from tvb.basic.logger.builder import get_logger
from tvb.basic.profile import TvbProfile
from tvb.config.init.datatypes_registry import populate_datatypes_registry
from tvb.core.services.simulator_serializer import SimulatorSerializer


def do_operation_launch(simulator_gid, input_folder, available_disk_space):
    log = get_logger('tvb.core.operation_hpc_launcher')
    try:
        log.debug("Preparing HPC launch for simulation with id={}".format(simulator_gid))
        populate_datatypes_registry()
        TvbProfile.current.hpc.HPC_INPUT_FOLDER = input_folder
        view_model = SimulatorSerializer().deserialize_simulator(simulator_gid, input_folder)
        adapter_instance = SimulatorAdapter()
        adapter_instance.storage_path = input_folder
        adapter_instance.configure(view_model)
        # adapter_instance._ensure_enough_resources(available_disk_space, view_model)
        result = adapter_instance.launch(view_model)
        if not isinstance(result, (list, tuple)):
            result = [result, ]
        # adapter_instance.__check_integrity(result)

    except Exception as excep:
        log.error("Could not execute operation {}".format(str(sys.argv[1])))
        log.exception(excep)


if __name__ == '__main__':
    TvbProfile.set_profile(TvbProfile.WEB_PROFILE, True)

    simulator_gid = sys.argv[1]
    input_folder = sys.argv[2]
    available_disk_space = sys.argv[3]

    do_operation_launch(simulator_gid, input_folder, available_disk_space)