from django.db import migrations

MSIL = 'Maruti Suzuki India Limited'

# name -> designation (taken from the APAC23 brochure, pages 6-8)
DESIGNATION = {
    'Mr. C.V. Raman': f'Executive Committee Member & Former CTO, {MSIL}',
    'Dr. G. Nagarajan': 'President, SAEINDIA, & Independent Director, SPEL Semiconductor Ltd.',
    'Mr. Javaji Munirathnam': 'Senior VP, SAEINDIA, & Founder and CEO Javaji M Consulting',
    'Mrs. Rashmi Urdhwareshe': 'Former Director, ARAI and Independent, & Director, STL (Sterling Tools)',
    'Dr. Reji Mathai': 'Director, Automotive Research Association of India (ARAI)',
    'Mr. Saurabh Dalela': 'Director, ICAT',
    'Dr. Manish Jaiswal': 'Director, NATRAX',
    'Mr. Guruprasad Mudlapur': 'President, Bosch Group in India and Managing Director, Bosch Ltd',
    'Mr. Murli. M. Iyer': 'Founding Member & Global Advisor, SAEINDIA President & CEO, Global Advisory Group LLC',
    'Mr. Inala Veerbhadra Rao': 'Distinguished Fellow, TERI',
    'Mr. Tarun Aggarwal': f'Sr EO - Head of Engineering, {MSIL}',
    'Mr. R. Velusamy': 'President, Automotive Technology & Product Development, M&M Ltd',
    'Dr. Saravanan': 'President & Chief Technology Officer, Ashok Leyland',
    'Dr. Tapan Sahoo': f'Executive Officer, {MSIL}',
    'Dr. Arun Jaura': 'Chief Technology Officer, JK Tyre & Industries',
    'Mr. N. Balasubramanian': 'Vice President - Product Engineering, RNTBCI',
    'Mr. Anurag Garg': 'Managing Director & Country Head India, Vitesco Technologies (Retd.)',
    'Mr. Rakesh Bidre': 'Vice President, TCS',
    'Ms. Latha Chembrakalam': 'Founder & CEO, AutoAscend Pvt. Ltd.',
    'Mr. Dinesh Tyagi': 'Founder & Managing Director, Dinty Autotech Pvt. Ltd.',
    'Mr. N. R. Girish': 'Vice President, R&D E-Mobility Asia Pacific, Schaeffler',
    'Mr. Dinesh Shyamsundar': 'CTO, EVage Automotive Pvt. Ltd.',
    'Dr. A S Ramadhas': 'Director, GARC',
    'Mr. Anoop Bhat': f'Executive Officer, {MSIL}',
    'Mr. Deepak Sawkar': f'Senior VP, {MSIL} (Retd.)',
    'Dr. Madhusudan Joshi': 'Head - Technology & Business, ICAT',
    'Mr. S. Ramanathan': 'Managing Director, Automotive Test Systems (ATS)',
    'Mr. M. Dhananjayan': 'Founder & CEO, Focus Engineering',
    'Mr. S. Damodaran': 'CEO, ChipEdge Technologies Pvt. Ltd.',
    'Mr. Sanjay Nibhandhe': 'Professor of Practice, Sri Vishnu Education Society',
    'Mr. Mahesh Babu': 'Managing Director - Olectra Greentech Limited',
    'Mr. Chris Mason': 'Chief Executive Officer, FISITA',
    'Mr. Abhijit Bora': f'Vice President, {MSIL}',
    'Mr. Nishant Sarna': f'Sr General Manager, {MSIL}',
    'Dr. B. V. Shamsundara': 'Senior Deputy Director, ARAI',
    'Mr. Praveensingh Jadhav': f'General Manager, {MSIL}',
    'Mr. Ajay Kumar': f'Sr. VP, {MSIL}',
    'Mr. Arun Kumar Goel': 'VP, Subros (Retd.)',
    'Mr. Pritam Singh': 'Sr. Manager, ICAT',
    'Mr. Piyush Jain': f'Sr. General Manager, {MSIL}',
    'Mr. Saurabh Maggu': f'General Manager, {MSIL}',
    'Mr. Prashant Vijay': 'Deputy General Manager - ICAT',
    'Mr. Jayawant Hardikar': 'Head - CMVR, ICAT',
    'Mr. C. Pradeep': 'Associate Director, OLA Electric Technologies',
    'Mr. N. K. Vaidya': 'Senior General Manager, Tata Motors',
    'Mr. Prakash Sardesai': 'Vice President, Professional & Faculty Development Board, SAEINDIA',
    'Mr. U. D. Bhangale': 'Executive Director, SAEINDIA Northern Section',
    'Mr. Abhishek Thakur': 'Executive, ICAT',
    'Dr. K. C. Vora': 'Director Auto CoE, NAMTECH',
    'Mr. R. Vijayalayan': 'Senior Manager, MathWorks',
    'Mr. Vijai Gopalakrishnan': 'Senior Network Consultant, TCS',
    'Ms. Ujjwala Karle': 'Deputy Director - Technology Group, ARAI',
    'Ms. Rajni Bagga': f'General Manager, {MSIL}',
    'Ms. Abha Rani': f'General Manager, {MSIL}',
    'Mr. Avinash Gupta': f'General Manager, {MSIL}',
    'Mr. Amit Karwal': 'Deputy General Manager, ICAT',
    'Mr. Prashant Vishe': 'Senior Manager, ICAT',
    'Mr. Deepak Joshi': 'Manager, ICAT',
    'Mr. Gopal Singh Rathore': 'Deputy Manager, ICAT',
    'Mr. Sitikantha Padhy': 'Manager, ICAT',
    'Dr. N. Karuppaiah': 'Senior Project Advisor, CAAR - IIT Madras',
    'Mr. Saravanan Thulasi': 'Technical Information Specialist, John Deere',
    'Mr. Ankit Trivedi': 'Manager, ICAT',
    'Mr. Avnish Gosain': f'Vice President, {MSIL}',
}

TP = 'Tech. & Publication'

COMMITTEES = [
    ('Steering Committee', [
        ('Mr. C.V. Raman', 'Patron'), ('Dr. G. Nagarajan', 'SC Chair'),
        ('Mr. Javaji Munirathnam', 'Member'), ('Mrs. Rashmi Urdhwareshe', 'Member'),
        ('Dr. Reji Mathai', 'Member'), ('Mr. Saurabh Dalela', 'OC - Chair'),
        ('Dr. Manish Jaiswal', 'Member'), ('Mr. Guruprasad Mudlapur', 'Member'),
        ('Mr. Murli. M. Iyer', 'Member'), ('Mr. Inala Veerbhadra Rao', 'Member'),
        ('Mr. Tarun Aggarwal', 'Member'), ('Mr. R. Velusamy', 'Member'),
        ('Dr. Saravanan', 'Member'), ('Dr. Tapan Sahoo', 'Member'),
        ('Dr. Arun Jaura', 'Member'), ('Mr. N. Balasubramanian', 'Member'),
        ('Mr. Anurag Garg', 'Member'), ('Mr. Rakesh Bidre', 'Member'),
        ('Ms. Latha Chembrakalam', 'Member'), ('Mr. Dinesh Tyagi', 'Member'),
        ('Mr. N. R. Girish', 'Member'), ('Mr. Dinesh Shyamsundar', 'Member'),
        ('Dr. A S Ramadhas', 'Member'), ('Mr. Anoop Bhat', 'Co Convenor'),
        ('Mr. Deepak Sawkar', 'Chair - Technical & Publication'),
        ('Dr. Madhusudan Joshi', 'Member'), ('Mr. S. Ramanathan', 'Chair - Event Management'),
        ('Mr. M. Dhananjayan', 'Chair - TechHive'), ('Mr. S. Damodaran', 'Chair - Media & Comm.'),
        ('Mr. Sanjay Nibhandhe', 'Chair - Industry Interface'),
        ('Mr. Mahesh Babu', 'Member'), ('Mr. Chris Mason', 'Member'),
    ]),
    ('Organizing Committee', [
        ('Mr. Saurabh Dalela', 'Chair'), ('Dr. Madhusudan Joshi', 'Convenor'),
        ('Mr. Anoop Bhat', 'Co Convenor'), ('Mr. M. Dhananjayan', 'Secretariat & Chair - TechHive'),
        ('Mr. Abhijit Bora', 'Core Member'), ('Mr. Nishant Sarna', 'Core Member'),
        ('Dr. B. V. Shamsundara', 'Core Member'), ('Mr. Praveensingh Jadhav', 'Core Member'),
        ('Mr. Deepak Sawkar', f'Chair - {TP}'), ('Mr. Ajay Kumar', f'Co Chair - {TP}'),
        ('Mr. Arun Kumar Goel', f'Co Chair - {TP}'), ('Mr. S. Ramanathan', 'Chair - Event Management'),
        ('Mr. Pritam Singh', 'Co Chair - Event Management'), ('Mr. Piyush Jain', 'Co Chair - Event Management'),
        ('Mr. Saurabh Maggu', 'Member - Event Management'), ('Mr. S. Damodaran', 'Chair - Media & Comm.'),
        ('Mr. Prashant Vijay', 'Chair - Finance Committee'), ('Mr. Jayawant Hardikar', 'Chair - Sponsorship'),
        ('Mr. C. Pradeep', 'Co Chair - TechHive'), ('Mr. N. K. Vaidya', 'Member'),
        ('Mr. Prakash Sardesai', 'Member'), ('Mr. U. D. Bhangale', 'Member'),
        ('Mr. Abhishek Thakur', 'Member - Event Management'),
        ('Mr. Sanjay Nibhandhe', 'Chair - Industry Interface'),
        ('Dr. K. C. Vora', 'Chair - Institute Interface'),
    ]),
    ('Technical Committee', [
        ('Mr. Deepak Sawkar', f'Chair - {TP}'), ('Mr. Ajay Kumar', f'Co Chair - {TP}'),
        ('Mr. Arun Kumar Goel', f'Co Chair - {TP}'), ('Mr. R. Vijayalayan', f'Member - {TP}'),
        ('Mr. Vijai Gopalakrishnan', f'Member - {TP}'), ('Ms. Ujjwala Karle', f'Member - {TP}'),
        ('Ms. Rajni Bagga', f'Member - {TP}'), ('Ms. Abha Rani', f'Member - {TP}'),
        ('Mr. Avinash Gupta', f'Member - {TP}'), ('Mr. Amit Karwal', f'Member - {TP}'),
        ('Mr. Prashant Vishe', f'Member - {TP}'), ('Mr. Prakash Sardesai', f'Member - {TP}'),
        ('Mr. Deepak Joshi', f'Member - {TP}'), ('Mr. Gopal Singh Rathore', f'Member - {TP}'),
        ('Mr. Sitikantha Padhy', f'Member - {TP}'), ('Dr. N. Karuppaiah', f'Member - {TP}'),
        ('Mr. Saravanan Thulasi', f'Member - {TP}'), ('Mr. Ankit Trivedi', f'Member - {TP}'),
        ('Mr. Avnish Gosain', f'Member - {TP}'),
    ]),
]


def seed(apps, schema_editor):
    Section = apps.get_model('core', 'CommitteeSection')
    Committee = apps.get_model('core', 'Committee')
    Member = apps.get_model('core', 'CommitteeMember')
    Role = apps.get_model('core', 'CommitteeRole')

    section, created = Section.objects.get_or_create(pk=1)
    if not created:
        return
    members = {}
    for c_order, (title, entries) in enumerate(COMMITTEES, start=1):
        committee = Committee.objects.create(section=section, title=title, order=c_order)
        for r_order, (name, role) in enumerate(entries, start=1):
            if name not in members:
                members[name] = Member.objects.create(name=name, designation=DESIGNATION[name])
            Role.objects.create(member=members[name], committee=committee, role=role, order=r_order)


class Migration(migrations.Migration):
    dependencies = [('core', '0014_committees')]
    operations = [migrations.RunPython(seed, migrations.RunPython.noop)]
