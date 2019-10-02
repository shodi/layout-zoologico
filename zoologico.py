# map_coloring.py
# From Classic Computer Science Problems in Python Chapter 3
# Copyright 2018 David Kopec
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from csp import Constraint, CSP
from typing import Dict, List, Optional


class ZooLayoutConstraint(Constraint[str, str]):
    def __init__(self, animal1: str, animal2: str, amigos: bool = False) -> None:
        super().__init__([animal1, animal2])
        self.animal1: str = animal1
        self.animal2: str = animal2
        self.amigos: bool = amigos

    def check_global_constraint(self, assignment: Dict[str, str]) -> bool:
        leao = assignment.get('Leao')
        tigre = assignment.get('Tigre')
        antilope = assignment.get('Antilope')
        if not leao or not tigre or not antilope:
            return True
        if leao == 1:
            if (antilope + 1 != leao and antilope + 1 != tigre) and\
                (antilope - 1 != leao and antilope - 1 != tigre):
                return True 
        return False

    def satisfied(self, assignment: Dict[str, str]) -> bool:
        if self.animal1 not in assignment or self.animal2 not in assignment:
            return True
        if not self.check_global_constraint(assignment):
            return False
        if self.amigos:
            return assignment[self.animal1] == assignment[self.animal2]
        else:
            return assignment[self.animal1] != assignment[self.animal2]


if __name__ == '__main__':
    variables: List[str] = ['Leao', 'Antilope', 'Hiena',
            'Tigre', 'Pavao', 'Suricate', 'Javali']
    domains: Dict[str, List[str]] = {}
    for variable in variables:
        domains[variable] = [1, 2, 3, 4]
    csp: CSP[str, str] = CSP(variables, domains)
    csp.add_constraint(ZooLayoutConstraint('Leao', 'Tigre'))
    csp.add_constraint(ZooLayoutConstraint('Suricate', 'Javali', True))
    csp.add_constraint(ZooLayoutConstraint('Hiena', 'Tigre', True))
    csp.add_constraint(ZooLayoutConstraint('Tigre', 'Suricate'))
    csp.add_constraint(ZooLayoutConstraint('Tigre', 'Javali'))
    csp.add_constraint(ZooLayoutConstraint('Tigre', 'Pavao'))
    csp.add_constraint(ZooLayoutConstraint('Tigre', 'Antilope'))
    csp.add_constraint(ZooLayoutConstraint('Leao', 'Antilope'))
    csp.add_constraint(ZooLayoutConstraint('Leao', 'Pavao'))
    solution: Optional[Dict[str, str]] = csp.backtracking_search()
    if solution is None:
        print('No solution found!')
    else:
        print(solution)