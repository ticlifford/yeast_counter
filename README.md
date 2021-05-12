# yeast_counter
This is an app to count yeast cells from a hemocytometer image.

## premise
Counting yeast cells typically involves making a dilution with methylene blue which turns dead cells blue.
Then, you put the dilution under a microscope and count the dead and living cells. This tells you two things.
It tells you the percent of viable cells, and the concentration of viable cells. 

## how it works
![test_image](yeast.jpg)

You start with an image from your microscope. This is produced by creating a 1:100 dilution by taking 1ml of your yeast and 99ml of distilled water/methylene blue solution.

![test_image](mask.jpg)

This program filters out the blue cells and counts them. It begins with a mask like this, and then counts the contours.

![test_image](blue_cells.jpg)

Here you can see the results. The red dots are identified dead cells. The methylene blue penetrates dead cells but doesn't disrupt the living ones. As you can see, its pretty accurate.
