# This file is part of Indico.
# Copyright (C) 2002 - 2016 European Organization for Nuclear Research (CERN).
#
# Indico is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 3 of the
# License, or (at your option) any later version.
#
# Indico is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Indico; if not, see <http://www.gnu.org/licenses/>.

from __future__ import unicode_literals

from flask import request

from indico.modules.events.timetable.legacy import TimetableSerializer
from indico.modules.events.timetable.views import WPDisplayTimetable
from MaKaC.common.fossilize import fossilize
from MaKaC.fossils.conference import IConferenceEventInfoFossil
from MaKaC.webinterface.rh.conferenceDisplay import RHConferenceBaseDisplay


class RHTimetable(RHConferenceBaseDisplay):
    def _checkParams(self, params):
        RHConferenceBaseDisplay._checkParams(self, params)
        self.layout = request.args.get('layout')
        if not self.layout:
            self.layout = request.args.get('ttLyt')

    def _process(self):
        event_info = fossilize(self._conf, IConferenceEventInfoFossil, tz=self._conf.tz)
        event_info['isCFAEnabled'] = self._conf.getAbstractMgr().isActive()
        timetable_data = TimetableSerializer().serialize_timetable(self.event_new)
        return WPDisplayTimetable.render_template('display.html', self._conf, event_info=event_info,
                                                  timetable_data=timetable_data, timetable_layout=self.layout)