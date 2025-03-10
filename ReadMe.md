# Dedupe
Currently I have a distractor and duplicate generator. In general the duplicates are reasonably good matches even if they really poorly match on my created model (the brute force model). The distractors on the other hand are mostly unrealistic....but for what it's worth they provide some with somewhat strong matches on my created model that are bad still. Thus, while the common distractor should probably be sorted as a non duplicate and the duplicates are expected generally to be duplicates, there can be variations such as distractors that know so much information about a person that they really are at least masquerading as that person....

## Patterns
### Patterns Considered Duplicates
#### Pattern 1 (Unless One is Junior and the Other is Senior With A Serious Breach of ID... They've Got to Be the Same Person with a Serious Notation Error)
[32.0, 4.0, 4.0, 8.0, 4.0, 40.0, 16.0, 16.0, nan]
['Richard Simpson', '911 Mario Trafficway Apt. 252', 'Adamburgh', 'Ohio', np.float64(92492.0), '12797798148x9099', '663-41-2408', 'curtistate@example.net', '1955-07-17', np.int64(-1)]
['Richard Simpson', '911 Mario Trafficway Apt. 252', 'Adamburgh', 'Ohio', np.float64(92492.0), '12797798148x9099', '663-41-2408', 'curtistate@example.net', '1946-10-09', np.int64(-1)]
['Joanna Lang', '111 Laura Mountains', 'West Candice', 'Vermont', np.float64(68116.0), '0019975191278x6938', '285-84-0146', 'stacy57@example.org', '2003-07-03', np.int64(-1)]
['Joanna Lang', '111 Laura Mountains', 'West Candice', 'Vermont', np.float64(68116.0), '0019975191278x6938', '285-84-0146', 'stacy57@example.org', '1971-03-21', np.int64(-1)]
['Anthony Coffey', '7582 Jeffrey Causeway', 'Danamouth', 'Arkansas', np.float64(52648.0), '14372841531x66941', '750-88-9010', 'sarah13@example.org', '1968-04-22', np.int64(-1)]
['Anthony Coffey', '7582 Jeffrey Causeway', 'Danamouth', 'Arkansas', np.float64(52648.0), '14372841531x66941', '750-88-9010', 'sarah13@example.org', '1986-11-15', np.int64(-1)]

#### Pattern 2 (99% certainty that one city was just written down wrong... .99 that they moved to the same street address in a different city and the rest for jr and sr)
[32.0, 4.0, 3.0, 8.0, nan, 40.0, 16.0, 16.0, 40.0]
['Christopher Pierce', '284 Johnson Prairie', 'Hopkinsmouth', 'New Jersey', np.float64(79739.0), '14796185731x3819', '548-79-4787', 'josephrowe@example.net', '1968-06-09', 
np.int64(-1)]
['Christopher Pierce', '284 Johnson Prairie', 'Summersmouth', 'New Jersey', np.float64(41415.940721220846), '14796185731x3819', '548-79-4787', 'josephrowe@example.net', '1968-06-09', np.int64(-1)]
['Daniel White', '03808 Jose Passage Suite 
336', 'North Jennifertown', 'Indiana', np.float64(97822.0), '12619188508x7942', '001-09-6103', 'elizabeth15@example.net', '1990-12-08', np.int64(-1)]
['Daniel White', '03808 Jose Passage Suite 
336', 'Kimtown', 'Indiana', np.float64(72980.02579191187), '12619188508x7942', '001-09-6103', 'elizabeth15@example.net', '1990-12-08', np.int64(-1)]
['Daniel White', '03808 Jose Passage Suite 
336', 'North Jennifertown', 'Indiana', np.float64(97822.0), '12619188508x7942', '001-09-6103', 'elizabeth15@example.net', '1990-12-08', np.int64(-1)]
['Daniel White', '03808 Jose Passage Suite 
336', 'Kimtown', 'Indiana', np.float64(72980.02579191187), '12619188508x7942', '001-09-6103', 'elizabeth15@example.net', '1990-12-08', np.int64(-1)]

#### Pattern 3 (50% Related???? 50% Same Person that Changed their Name??? --- most information belongs to one person...)
[0.0, 4.0, 4.0, 8.0, 4.0, 40.0, 16.0, 16.0, 40.0]
['Jennifer Smith', '23226 West Knoll Apt. 861', 'West Stephaniehaven', 'California', np.float64(82954.0), '18813534423x997', '743-27-1713', 'lauraharris@example.org', '1944-03-10', np.int64(-1)]
['Michael Warner', '23226 West Knoll Apt. 861', 'West Stephaniehaven', 'California', np.float64(82954.0), '18813534423x997', '743-27-1713', 'lauraharris@example.org', '1944-03-10', np.int64(-1)]
['Michelle Grant', '034 Jeffrey Mountains Suite 483', 'Lynnberg', 'South Dakota', np.float64(65822.0), '13785514120', '449-50-3783', 'drew28@example.org', '1969-07-24', np.int64(-1)]
['Ryan Shepherd', '034 Jeffrey Mountains Suite 483', 'Lynnberg', 'South Dakota', np.float64(65822.0), '13785514120', '449-50-3783', 'drew28@example.org', '1969-07-24', np.int64(-1)]
['Grace Nguyen', '517 Maureen Prairie', 'New Richardfurt', 'North Carolina', np.float64(11136.0), '16505668880x3032', '182-11-2606', 'christopher59@example.org', '1967-09-04', np.int64(-1)]
['Jim Tucker', '517 Maureen Prairie', 'New 
Richardfurt', 'North Carolina', np.float64(11136.0), '16505668880x3032', '182-11-2606', 'christopher59@example.org', '1967-09-04', np.int64(-1)]

#### Pattern 4 (Natural???? Something is in error probably... Wrong address for ordering for a different person???)
[0.0, 4.0, 0.0, 8.0, 4.0, 40.0, 16.0, 16.0, nan]
['Brian Harris', '6599 Martin Freeway', 'Lake Eric', 'Louisiana', 17389.0, '0019192950501x085', '773-76-8065', 'bellmatthew@example.org', '1966-08-09', -1]
['Aaron Richard', '6599 Martin Freeway', 'Reyesport', 'Louisiana', 17389.0, '0019192950501x085', '773-76-8065', 'bellmatthew@example.org', '1958-06-24', -1]
['Linda Blackburn', '64689 Michael Neck Apt. 716', 'South John', 'California', 3939.0, '16253973817x196', '381-05-6479', 'gramirez@example.net', '2004-12-18', -1]
['Rachel Chavez', '64689 Michael Neck Apt. 716', 'Port Destiny', 'California', 3939.0, '16253973817x196', '381-05-6479', 'gramirez@example.net', '1965-09-21', -1]
['Thomas Stein', '61757 Laura Common', 'South Jessica', 'Vermont', 27869.0, '17863012591x21313', '001-26-3353', 'gomezkatie@example.com', '1945-01-24', -1]
['Cassandra Lewis', '61757 Laura Common', 'Hudsonborough', 'Vermont', 27869.0, '17863012591x21313', '001-26-3353', 'gomezkatie@example.com', '1996-09-06', -1]

#### Pattern 5 (Incorrect City?)
[32.0, 4.0, 0.0, 8.0, 4.0, 40.0, 16.0, 16.0, 40.0]
['Bobby Hartman', '0878 Dominguez Inlet Suite 543', 'Port Thomas', 'North Carolina', 91004.0, '14053652469', '070-31-0616', 'cmartinez@example.com', '2003-06-19', -1]
['Bobby Hartman', '0878 Dominguez Inlet Suite 543', 'Port Ashleyview', 'North Carolina', 91004.0, '14053652469', '070-31-0616', 'cmartinez@example.com', '2003-06-19', -1]
['David Rose', '412 Martin Club Apt. 135', 'West Summerport', 'Nevada', 60652.0, '12285032044', '550-84-4188', 'taylorstephanie@example.net', '1977-04-04', -1]
['David Rose', '412 Martin Club Apt. 135', 'Taylorfurt', 'Nevada', 60652.0, '12285032044', '550-84-4188', 'taylorstephanie@example.net', '1977-04-04', -1]
['Bailey Flores', '97057 Stanley Harbor Apt. 602', 'East Kristinhaven', 'Idaho', 45512.0, '13357137158x228', '258-35-3591', 'amberhayes@example.net', '1999-01-27', -1]
['Bailey Flores', '97057 Stanley Harbor Apt. 602', 'Port Karltown', 'Idaho', 45512.0, '13357137158x228', '258-35-3591', 'amberhayes@example.net', '1999-01-27', -1]

### Patterns Considered Non Duplicates
#### Pattern 1 (Serious Identity Theft Concerns....probably not a duplicate)
[0.0, 0.0, 0.0, 0.0, nan, 40.0, nan, nan, nan]
['Nicole Thomas', '78934 Kelley Motorway', 
'South Makayla', 'Idaho', np.float64(4908.0), '0017698056184x6946', '794-24-1277', 'nicholasbuck@example.org', '1972-08-13', np.int64(-1)]
['Timothy Morgan', '8422 Williams Harbor Apt. 431', 'Steelehaven', 'West Virginia', np.float64(67228.978080269), '19367391507', '794-24-1277', 'haydensavage@example.net', '2005-04-04', np.int64(-1)]
['Donna Combs', '604 Torres Mount', 'Lake Markfurt', 'Pennsylvania', np.float64(62374.0), '19454204461x2620', '693-88-4023', 'timothymiller@example.com', '2001-05-05', np.int64(-1)]
['David Hopkins', '87545 Bowen Ferry Apt. 430', 'New Teresaside', 'Alaska', np.float64(58083.31394168049), '13676900995x41534', '693-88-4023', 'daviessteven@example.net', '1980-04-15', np.int64(-1)]
['Danielle Jones', '050 Clark Brooks Apt. 919', 'Port Douglasberg', 'Nebraska', np.float64(33658.0), '16603919012x449', '325-38-4764', 'taylor01@example.com', '2002-04-30', np.int64(-1)]
['Johnny Olson', '74503 Janet Junction Apt. 198', 'Stevenland', 'Colorado', np.float64(73693.28357651556), '18275249964x93375', '325-38-4764', 'williamcoleman@example.com', '1956-12-06', np.int64(-1)]
[0.0, 4.0, 0.0, 8.0, 4.0, 40.0, 16.0, 16.0, nan]
['Tami Richards', '3829 Jennifer Inlet', 'South Erikafurt', 'Maine', np.float64(13490.0), '16255523216x337', '151-16-8603', 'rodriguezkristopher@example.net', '2001-08-27', np.int64(-1)]
['Casey Waller', '3829 Jennifer Inlet', 'Patrickside', 'Maine', np.float64(13490.0), '16255523216x337', '151-16-8603', 'rodriguezkristopher@example.net', '1953-06-01', np.int64(-1)]
['Tami Richards', '3829 Jennifer Inlet', 'South Erikafurt', 'Maine', np.float64(13490.0), '16255523216x337', '151-16-8603', 'rodriguezkristopher@example.net', '2001-08-27', np.int64(-1)]
['Casey Waller', '3829 Jennifer Inlet', 'Patrickside', 'Maine', np.float64(13490.0), '16255523216x337', '151-16-8603', 'rodriguezkristopher@example.net', '1953-06-01', np.int64(-1)]
['Anna Johnson', '06407 Stacy Cliffs Apt. 060', 'New Geraldbury', 'Indiana', np.float64(17945.0), '12337058235x297', '747-04-2114', 'longpatricia@example.org', '2006-10-14', np.int64(-1)]
['Jessica Hernandez', '06407 Stacy Cliffs Apt. 060', 'East Sheenaberg', 'Indiana', np.float64(17945.0), '12337058235x297', '747-04-2114', 'longpatricia@example.org', '1945-03-03', np.int64(-1)]