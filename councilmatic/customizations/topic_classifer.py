
def topic_classifier(title) :
    title = title.encode('ascii', 'ignore')

    if 'damage to vehicle' in title.lower() or 'damage to vhicle' in title.lower():
        return ['Routine', 'Damage to vehicle claim']

    if 'Damage to property claim' in title :
        return ['Routine', 'Damage to property claim']

    if 'Excessive water rate claim' in title :
        return ['Routine', 'Excessive water rate claim']

    if 'Issuance of permits for sign(s)/signboard(s)' in title :
        return ['Routine', 'Sign permits']

    if title.lower().startswith(('cancellation of warrants',)) :
        return ['Non-Routine', 'Cancellation of Warrants for Collection']

    if title.startswith(('No Cruising',)) :
        return ['Non-Routine', 'No Cruising Zone']

    if title.startswith(('Free permit', 
                         'Fee Exemption',
                         'Refund of fee',
                         'Waiver of public way use permit fee',
                         'Fee exemption',
                         'Waiver of community identifier sign permit fee',
                         'Waiver of Fees', 
                         'Waiver of fee',
                         'Waiver of special event',
                         'Exemption of public way use',
                         'Cancellation of public way use permit fee', 
                         'Waiver of permit fee',
                         'Waiver of public use permit fee',
                         'License Fee Exemption',
                         'License fee exemption')) :
        return ['Non-Routine', 'Free Permits or License']

    if title.startswith(('Donation', 'Donate')) :
        return ['Non-Routine', 'Donation']

    if title.startswith(('Sidewalk Cafe',
                         'Sidewalk cafe')) :
        return ['Routine', 'Sidewalk cafe']

    if title.startswith(('Loading/Standing/Tow Zone',
                         'Loading/Standing/Tow',
                         'Amendment of Loading',
                         'Repeal Loading',
                         'Tow Zones',
                         'Tow Zone - Street Cleaning',
                         'Tow Zone(s) - Street Cleaning',
                         'Traffic Lane - Tow/Away Zone',
                         'Traffic Lane',
                         'Traffic Lane Tow',
                         'Loading Zone',
                         'Traffic Lane Tow-Away Zones')) : 
        return ['Routine', 'Loading/Standing/Tow Zone']

    if title.startswith(('Speed hump',)) :
        return ['Non-Routine', 'Speed Hump']

    if title.startswith(('Support of Class 6(b)',
                         'Support of Class L',
                         'Class C',
                         'Class L',
                         'Designation of Class 7',
                         'Support of Class C',
                         'Expression of consent for Class 7')) :
        return ['Non-Routine', 'Tax Incentives']

    if 'Subdivision' in title or 'Resubdivision' in title:
        return ['Non-Routine', 'Subdivison']


    if title.startswith(('Congratulations extended', 
                         'Congratulations and best wishes',
                         'Congratulation',
                         'Congratulations to',
                         'Congradulations',
                         'Congraulations',
                         'Recoginition',
                         'congratulations',
                         'Commemoration of', 
                         'Tribute to', 
                         'Declaraton',
                         'Posthumous gratitude',
                         'Commendations extended to',
                         'Gratitude',
                         'Best wishes extended',
                         'Gratitude to',
                         'Grattitude extended',
                         'Condolences extended',
                         'Recognition extended',
                         'Posthumous congratulations',
                         'Expression of condolence',
                         'Recognition of',
                         'Expression sympathy',
                         'Honoring',
                         'Welcome extended')) or 'declaration' in title.lower() :
        return ['Routine', 'Honorific']

    if 'commemorative' in title.lower() :
        return ['Routine', 'Honorific Marker']


    if title.startswith(('Conduct of sidewalk sale', 
                         'Sidewalk sale', 
                         'Conduct of Sidewalk Sale')) :
        return ['Non-Routine', 'Sidewalk Sale']

    if title.startswith(('Residential permit parking', 
                         'Residential Permit Parking',
                         'Amendment of residential', 
                         'Residential Parking',
                         'Residential parking',
                         'Buffer zone',
                         'Buffer Zone')) :
        return ['Routine', 'Residential permit parking']

    if title.startswith(('Service drive', 'Service Drive')) :
        return ['Non-Routine', 'Service Drive/Diagonal Parking']

    if title.startswith(('Traffic sign', 
                         'Traffic Signs',
                         'Traffic Sign(s)',
                         'Traffic Warning Signs',
                         'Traffic Warning Sign and/or Signals',
                         'Traffic warning sign and/or signals',
                         'Traffic sign',
                         'Miscellaneous Signs')) :
        return ['Routine', 'Traffic signs and signals']

    if title.startswith(('Senior citizen sewer',
                         'Senior Citizen Sewer',
                         'Senior Citizen Sewer Refunds')) :
        return ['Routine', 'Senior citizen sewer refund']

    if 'easement agreement' in title.lower() :
        return ['Non-Routine', 'Easement Agreement']

    if 'tifworks' in title.lower() :
        return ['Non-Routine', 'TIFWorks']

    if ('neighborhood improvement program' in title.lower() 
        or 'neighborhood investment program' in title.lower()
        or 'tif-nip' in title.lower() ) :
        return ['Non-Routine', 'TIF Neighborhood Improvement Program']

    if 'neighborhood stabilization program' in title.lower() :
        return ['Non-Routine', 'Neighborhood Stabilization Program']

    if 'transfer of tif funds' in title.lower() or ('allocation of' in title.lower() and 'tif funds' in title.lower()):
        return ['Non-Routine', 'Transfer of TIF funds']


    if 'CDBG' in title or 'Community Development Block Grant ordinance' in title:
        return ['Non-Routine', 'Community Development Block Grant']

    if title.startswith(('Submission of public question')) :
        return ['Non-Routine', 'Ballot Questions']

    if title.startswith(('Grant(s) of privilege in public way',
                         'Grant of privlage in public',
                         'Grant of priviege',
                         'Grant(s) of privilege',
                         'Grant(s) of priviledge',
                         'Grants of Privilege in the Public Way',
                         'Grant of privilege in public way',
                         'Grant(s) of Privilege in Public Way',
                         'Amendment of grant(s) of privilege')) :
        return ['Routine', 'Grant of privilege in public way']

    if title.startswith(('Handicapped Parking Permit',
                         'Handicapped Permit Parking',
                         'Handicapped Parking',
                         'Handicapped parking permit',
                         'Handicapped permit parking')) :
        return ['Routine', 'Handicapped Parking Permit']

    if title.startswith(('Speed Limitation', 'Speed limitation')) :
        return ['Non-Routine', 'Speed Limits']

    if title.startswith(('Lease agreement')) :
        return ['Non-Routine', 'Lease agreement']

    if title.startswith(('Parking Meters', 
                         'Parking meters',
                         'Amendment of parking meters',
                         'Installation and removal of parking meters',
                         'Removal and relocation of parking meters')) :
        return ['Non-Routine', 'Parking Meters']
        
    if title.startswith(('Limited Local Access',)) :
        return ['Non-Routine', 'Limited Local Access']

    if title.startswith(('Parking prohibited',
                         'Amendment of parking prohibition',
                         'Parking Prohibited',
                         'Parking Prohibitited',
                         'Parking Limited',
                         'Parking Limitation',
                         'Parking limitation',
                         'Parking Restrictions',
                         'Parking limited',
                         'Amendment of parking limitation',
                         )) :
        return ['Routine', 'Parking Restrictions']

    if title.startswith('Amendment') and 'tif' in title.lower() and 'budget' in title.lower() :
        return ['Non-Routine', 'TIF Budget']

    if title.startswith(('Inspector General')) :
        return ['Non-Routine', "Inspector General"]


    if title.startswith(('Handicapped Parking Permit',
                         'Handicapped permit parking')) :
        return ['Routine', 'Handicapped Parking Permit']


    if title.startswith('Zoning Reclassification') :
        return ['Routine', 'Zoning Reclassification']

    if title.startswith('Awning(s)') :
        return ['Routine', 'Awnings']

    if title.startswith('Canopy(s)') :
        return ['Routine', 'Canopy']

    if title.startswith(('Cancellation of Water',
                         'Cancellation of water',
                         'Cancellation of Warrants for Water')) :
        return ['Routine', 'Cancellation of Water/Sewer']



    if title.startswith(('Tag day permit', 
                         'Tag days permit',
                         'Tag day pernmit',
                         'Tag day(s) permit')) :
        return ['Non-Routine', 'Tag Day Permits']

    if title.startswith(('Correction of City Council Journal',
                         'Correction of Journal')) :
        return ['Non-Routine', 'Correction of City Council Journal']

    if title.startswith(('Payment of',
                         'Payments of',
                         'Payment for various',
                         'Denying payment',
                         'Denials of Condo',
                         'Denials Condo',
                         'Denied Condo',
                         'Denied various claims',
                         'Various small claims',
                         'Small Claims',
                         'Denied condo',
                         'Denials of various',
                         'Denial of various',
                         'Payment of various small claims')) :
        return ['Non-Routine', 'Settlement of Claims']

    if title.startswith(('Closed to', 'Close to', 'Closure to vehic', 'Traffic closure')) :
        return ['Non-Routine', 'Traffic Closure']


    if title.startswith(('Honorary street designation',
                         'Designation of "Ed and Betty Gardner Street"',
                         'Dedication of')) :
        return ['Routine', 'Honorary street']


    if title.startswith(('Condominium claim',
                         'Condominium refuse',
                         'Condominium Claim')) :
        return ['Routine', 'Condo Claim']

    if title.startswith(('Call for hearing',)) :
        return ['Non-Routine', 'Call for Hearing']

    if title.startswith(('Transfer of Funds to Committee',
                         'Transfer of funds within Committee',
                         'Transfer of funds within the City Council Committee',
                         'Transfer of funds within the Committee',
                         'Transfer of Year 2013 funds within Committee',
                         'Transfer of funds to Committee')) :
        return ['Non-Routine', 'Transfer of Committee Funds']

    if title.startswith(('One Time Exception to Wrigley Field',
                         'One Time Exception to Wrigley',
                         'Amendment of Wrigley Field',
                         'Amendment of Night Game',
                         'One Time Exception to Night Game',
                         'Amendment of Wrigley Adjacent Area')) :
        return ['Non-Routine', 'Wrigley Field']

    if title.startswith(('Traffic Direction',
                         'Single Direction',
                         'One Way Traffic',
                         'One-Way Traffic',
                         'Repeal one-way',
                         'One-way traffic',
                         'Traffic direction')) :
        return ['Non-Routine', 'Traffic Direction']

    if title.startswith(('Free Permit', 'Refund of Fees')) :
        return ['Non-Routine', 'Free Permits']

    if title.startswith(('Collective Bargaining', 'Collective bargaining')) :
        return ['Non-Routine', 'Labor Agreement']

    if title.startswith(('Intergovernmental agreement', 
                         'Renewal of intergovernment',
                         'Intergovernment agreement',
                         'Amendment of intergovernmental agreement',
                         'Intergovernmental Agreement')) :
        return ['Non-Routine', 'Intergovernmental Agreement']

    if title.startswith(('Waiver of special event license',
                         'Waiver of annual public assembly fee',
                         'Waiver of permit fees',
                         'Wavier of special event tent',
                         'Waiver of street closure permit fee',
                         'Issue Special Event',
                         'Waiver of Special Event License')) :
        return ['Non-Routine', 'Waiver of Special Event License or Permits Fees']

    if 'motor fuel tax funds' in title.lower() :
        return ['Non-Routine', 'Motor Fuel Tax Funds']

    if title.startswith(('Settlement agreement', 
                         'Sylwia Marcincryk v.',
                         'Setttlement order',
                         'Settlement order',
                         'Judgement and Settlement Report',
                         'Judgements or settlements',
                         'Judgment and Settlement',
                         'Judgement or settlments',
                         'Judgement or Settlement Report')) :
        return ['Non-Routine', 'Settlement Agreement']

    if title.lower() == 'test' or title.lower().startswith(('system test', 'test')) :
        return ['Routine', 'Test']
    
    if title.startswith(('Removal of Taxicab Stand',
                         'Repeal of Taxicab Stand',
                         'Taxicab stand',
                         'Taxicab Stand',
                         'Amendment of taxicab',
                         'Amendment of Taxicab Stand',
                         'Establish Taxicab',
                         'Establishment of Taxicab Stand',
                         'Establishment of taxicab stand')) :
        return ['Non-Routine', 'Taxicab Stand']

    if title.startswith(('Appointment', 'Reappointment')) :
        return ['Non-Routine', 'Appointment']

    if title.startswith(('Issuance of special event license',)) :
        return ['Non-Routine', 'Special Event License']

    if title.startswith(('Waiver of special event raffle license',)) :
        return ['Non-Routine', 'Waiver of Special Event Raffle License Fees']

    if title.startswith(('Call for',
                         'Call upon',
                         'Expression of support',
                         'Support of',
                         'Expression of opposition',
                         'Denouncement',
                         'Condemnation of')) :
        return ['Non-Routine', 'Exhortation']

    if title.startswith(('Historical landmark fee',
                         'Landmark fee waiver')) :
        return ['Non-Routine', 'Historical Landmark Fee Waiver']

    if title.startswith(('Vacation', 'Amendment of vacation')) :
        return ['Non-Routine', 'Vacation of Public Street']

    if ('S.S.A.' in title or 'SSA' in title or 'Special Service No' in title 
        or 'special service area' in title.lower()) :
        return ['Non-Routine', 'Special Service Area']

    if 'pilot parking program' in title.lower() :
        return ['Non-Routine', 'Pilot Parking Program']
                         

    if title.startswith(('Permission to hold', 'Permission to Hold')) :
        return ['Non-Routine', 'Event Permission']

    if title.startswith(('Loan agreement', 
                         'Multi-family loan agreement',
                         'Loan assumption',
                         'Amendment of terms',
                         'Loan modification',
                         'Amendment of terms on loan agreement',
                         'Amendment of loan agreement',
                         'Amendment to loan agreement',
                         'Loan Agreement',
                         'Loan restructure')) :
        return ['Non-Routine', 'Loan Agreement']

    if (' Bonds' in title or ' bond issuance ' in title 
        or ' bond proceeds ' in title  or ' bonds ' in title) : 
        return ['Non-Routine', 'Bonds']

    if title.startswith(('Lease Agreement', 
                         'Lease agreement', 
                         'Sub-lease agreement',
                         'Amendment of lease')) :
        return ['Non-Routine', 'Lease Agreement']

    if title.startswith(('Traffic regulations',
                         'Traffic Regulations',
                         'Failed to Pass Traffic Regulation',
                         'Various traffic regulations',
                         'Construction of Traffic Circles')):
        return ['Non-Routine', 'Traffic Regulation']

    if title.startswith(('Expenditure of Open Space',
                         'Expenditure of open space')) :
        return ['Non-Routine', 'Open Space Imact Funds']

    if title.startswith(("Laborers' and Retirement Board",
                         'Retirement Board of Policemen',
                         'Retirement Board of Firemen')) :
        return ['Non-Routine', 'Pensions']

    if title.startswith(('Affordable Housing Plan')) :
        return ['Non-Routine', 'Affordable Housing']

    if title.startswith(('City Comptroller',
                         'City of Chicago Annual Financial Analysis',
                         'Comprehensive Annual Financial Report')) :
        return ['Non-Routine', 'Financial Reports']

    if title.startswith(('Sale of City-owned propert',
                         'Amendment of acquisition of property',
                         'Sale of City-owned Propert',
                         'Conveyance of City-owned prop',
                         'Approval of land sale',
                         'Acceptance of bid for property',
                         'Conveyance of City land',
                         'Conveyance of City propert',
                         'Land transfer',
                         'Transfer of Merchant Park property',
                         'Amendment to terms of previously authorized land transactions',
                         'Transfer of parcels',
                         'Transfer of property to',
                         'Acceptance of propert',
                         'Conveyance of propert',
                         'Amendment of land sale',
                         'Conveyance of open space land',
                         'Negotiated sale of City-owned property',
                         'Acquisition')) :
        return ['Non-Routine', 'Acquisition, Sale, and Conveyance of Property']

    if title.lower().startswith(('not-for-profit fee exemption',
                                 'sewer refund',
                                 'Refund of fee')) :
        return ['Non-Routine', 'Not-for-Profit Fee Exemption']

    if 'Annual Appropriation' in title :
        return ['Non-Routine', 'Annual Appropriation']

    if title.startswith(('Historical landmark designation',
                         'Correction to Chicago Landmark Designation')) :
        return ['Non-Routine', 'Historical Landmark']

    if '4-60-022' in title or '4-60-023' in title :
        return ['Non-Routine', 'Liquor and Package Store Restrictions']

    if '4-244-140' in title :
        return ['Non-Routine', 'Restrict Peddling']

    if 'small business improvement fund' in title :
        return ['Non-Routine', 'Small Business Improvement Fund']


    if title.startswith(('Amendment of Section',
                         'Amendment of Subsection',
                         'Amendment of Title',
                         'Amendment of various provisions of Municipal',
                         'Amendment of various sections of Municipal Code',
                         'Repeal of Section',
                         'Amendment of Municipal Code',
                         'Amendment to Municipal Code',
                         'Amendment of Chapter')) :
        return ['Non-Routine', 'Legislation']

    if title.startswith(('Fixed for next City Council Meeting',
                         'Time Fixed',
                         'Time Fixed for next City Council Meeting',
                         'Amending City Council meeting time')) :
        return ['Routine', 'Next Meeting']

    if title == '':
        return ['No Info']


    if title.startswith(('Industrial Permit Parking',
                         'Industrial permit parking')) :
        return ['Non-Routine', 'Industrial Permit Parking']

    if title.startswith(('Oath',)) :
        return ['Non-Routine', 'Oath of Office']

    if title.startswith(('Pay rate of hospital', 
                         'Payment of hospital and med')) :
        return ['Routine', 'Police and Firefighter Medical Bills']

    if title.startswith(('Independent Police Review',
                         'Police Review Authority',
                         'Police Board')) :
        return ['Non-Routine', 'Police Oversight']

    if title.startswith(('Vehicle weight',
                         'Vehicle weigh',
                         'Weight Limitation',
                         'Vehicle Weight', 
                         'Weigh Limitation')) :
        return ['Non-Routine', 'Vehicle Weight Limitation']

    if title.startswith(('Redevelopment agreement',
                         'Amendment to previous redevelopment agreement',
                         'Amendment of redevelopment agreement',
                         'First amendment to redevelopment agreement',
                         )) or 'associated redevelopment agreement' in title :
        return ['Non-Routine', 'Redevelopment Agreement']

    if title.lower().startswith(('exemption from',
                                 'exemption from')) :
        return ['Routine', 'Physical barrier exemption']

    if 'tax increment financing' in title.lower() :
        return ['Non-Routine', 'Tax Increment Financing']

    if 'redevelopment project area' in title.lower() :
        return ['Non-Routine', 'Redevelopment Project Area']

    if title.lower().startswith(('issuance of permit',
                                 'issuance of license')) :
        return ['Non-Routine', 'Issuance of License and Permits']



    return ['Non-Routine', 'Unclassified']
