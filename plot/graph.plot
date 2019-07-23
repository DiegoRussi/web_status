#!/usr/local/bin/gnuplot -persist

# Path to plot data result.csv:
filename = '/usr/local/bin/ENV[AUTH_TOKEN]_web_status/plot/result.csv'
# result.csv
#	title, result
#	Failtures, 123
#	Success, 1234

rowi = 1
rowf = 7

# obtain sum(column(2)) from rows `rowi` to `rowf`
set term png enhanced font arial 14 tiny size
set title "ENV[AUTH_TOKEN] Monitoring sites" font ",16"
set output "/tmp/pie_chart.png"
set datafile separator ','
#stats filename u 2 every ::rowi::rowf noout prefix "A"
stats filename u 2 noout prefix "A"     # get STATS_sum (sum of column 2)

# rowf should not be greater than length of file
rowf = (rowf-rowi > A_records - 1 ? A_records + rowi - 1 : rowf)

angle(x)=x*360/A_sum
percentage(x)=x*100/A_sum

# circumference dimensions for pie-chart
centerX=0
centerY=0
radius=1

# label positions
yposmin = 0.0
yposmax = 0.15*radius
xpos = 1.2*radius
ypos(i) = 0.7 + yposmax - i*(yposmax-yposmin)/(1.0*rowf-rowi)

#-------------------------------------------------------------------
# now we can configure the canvas
set style fill solid 1     # filled pie-chart
unset key                  # no automatic labels
unset tics                 # remove tics
unset border               # remove borders; if some label is missing, comment to see what is happening

set size ratio -1              # equal scale length
set xrange [-radius:1.7*radius]  # [-1:2] leaves space for labels
set yrange [-radius:radius]    # [-1:1]

#-------------------------------------------------------------------
pos = 0             # init angle
colour = 0          # init colour

# 1st line: plot pie-chart
# 2nd line: draw colored boxes at (xpos):(ypos)
# 3rd line: place labels at (xpos+offset):(ypos)
plot filename u (centerX):(centerY):(radius):(pos):(pos=pos+angle($2)):(colour=colour+1) every ::rowi::rowf w circle lc var,\
     for [i=0:rowf-rowi] '+' u (xpos):(ypos(i)) w p pt 5 ps 4 lc i+1,\
     for [i=0:rowf-rowi] filename u (xpos):(ypos(i)):(sprintf('%05.2f%% %s', percentage($2), stringcolumn(1))) every ::i+rowi::i+rowi w labels left offset 3,0
