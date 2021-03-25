##############################################################################
#
#    Copyright (C) 2015  ADHOC SA  (http://www.adhoc.com.ar)
#    All Rights Reserved.
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
{
    'name': 'Multi Store for Point of Sale',
    'version': '12.0.1.0.0',
    'category': 'Point Of Sale',
    'sequence': 14,
    'summary': '',
    'author': 'ADHOC SA, Giovanni Serra - GSLab.it',
    'website': 'www.adhoc.com.ar',
    'license': 'AGPL-3',
    'images': [],
    'depends': [
        'point_of_sale',
        'base_multi_store',
    ],
    'data': [
        'security/multi_store_security.xml',
        'views/pos_order_view.xml',
    ],
    'demo': [],
    'installable': True,
    'auto_install': True,
    'application': False,
}
