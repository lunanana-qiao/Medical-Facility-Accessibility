class Eve_medical_data:
    def __init__(self,id,people):
        self.medical_id=id

        self.S_people = people

        self.SUM_GR=0
        self.A_people = 0


        self.oSUM_GR = 0
        self.oA_people = 0


class Eve_social_data:
    def __init__(self, id):
        self.social_id = id
        self.adj=0

        self.SUM_GR_people = 0
        self.oSUM_GR_people = 0


class model:
    def __init__(self, total_people,old_people,S):
        self.total_people=total_people
        self.old_people=old_people
        self.S=S
        self.sum_peo=0.
        self.sum_old_peo=0.
        self.SUM_S=0.


class area:
    def __init__(self,name):
        self.name=name
        self.sum_people=0
        self.sum_old_people = 0
        self.serve_people_15=0
        self.serve_people_center_15 = 0
        self.serve_people_zhan_15 = 0
        self.serve_people_10 = 0
        self.serve_people_center_10 = 0
        self.serve_people_zhan_10 = 0
        self.serve_people_5 = 0
        self.serve_people_center_5 = 0
        self.serve_people_zhan_5 = 0

        self.serve_old_people_15 = 0
        self.serve_old_people_center_15 = 0
        self.serve_old_people_zhan_15 = 0
        self.serve_old_people_10 = 0
        self.serve_old_people_center_10 = 0
        self.serve_old_people_zhan_10 = 0
        self.serve_old_people_5 = 0
        self.serve_old_people_center_5 = 0
        self.serve_old_people_zhan_5 = 0
class pianqu(area):
    def __init__(self,name):
        area.__init__(self,name)


class jiedao:
    def __init__(self,name):
        area.__init__(self,name)
class shequ:
    def __init__(self,name):
        area.__init__(self,name)