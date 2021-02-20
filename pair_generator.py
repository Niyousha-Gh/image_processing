import os
import shutil
import random
import argparse
import sys

class GeneratePairs:

	""" Generate same and different pairs of images from index and others datasets """
	def __init__(self, index_dir, others_dir, outputs_dir):
       
		self.index_dir = index_dir.replace('\\', '/')
		self.others_dir = others_dir.replace('\\', '/')
		self.outputs_dir = outputs_dir.replace('\\', '/')


	def generate(self):
        	pair_number = self._generate_same_pairs()
        	self._generate_different_pairs(pair_number)


	def _generate_same_pairs(self):
		# Generate the same pairs

		# Create same folder in output_dir
		path = os.path.join(self.outputs_dir, 'same')
		
		try:  
    			os.mkdir(path)  
		except OSError as error:  
    			print(error)


		# Save the total number of same pairs
		pair_number = 0

		# Store matched images in mached_imags list
		for index_id in os.listdir(self.index_dir):
			
			matched_imgs = []
			matched_imgs.append(index_id)

			for others_id in os.listdir(self.others_dir):
				if index_id.split('.')[0] == others_id.split('_')[0]:
					matched_imgs.append(others_id)

			
			# Make pairs with all the same images
			for i in reversed(matched_imgs):
				for j in reversed(matched_imgs):
					if i is not j:
						pair_number = pair_number + 1
						self._make_folder(i, j, 'same', index_id)

				matched_imgs.remove(i)

		return pair_number


	def _make_folder(self, img_1, img_2, group, index_id=''):
		# Make new folders for new pairs.  
		# If one of the images is from index deirectory its value will be inserted to index variable
		
		# Check wether same pair folders should be created or different
		if group == 'same':
			folder_name = "same " + img_1.split('.')[0] + ' & ' + img_2.split('.')[0]
			des_dir = self.outputs_dir + '/same'

		else:
			folder_name = "different " + img_1.split('.')[0] + ' & ' + img_2.split('.')[0]
			des_dir = self.outputs_dir + '/different'

		path = os.path.join(des_dir, folder_name)
		
		try:  
    			os.mkdir(path)  
		except OSError as error:  
    			print(error)

		
		# Copy the images to the outputs folder
		if index_id == img_1:

			src_1 = self.index_dir + '/' + img_1

			shutil.copy(src_1, path)

			src_2 = self.others_dir + '/' + img_2

			shutil.copy(src_2, path)


		elif index_id == img_2:

			src_1 = self.others_dir + '/' + img_1

			shutil.copy(src_1, path)

			src_2 = self.index_dir + '/' + img_2

			shutil.copy(src_2, path)

		else:
			
			src_1 = self.others_dir + '/' + img_1

			shutil.copy(src_1, path)

			src_2 = self.others_dir + '/' + img_2

			shutil.copy(src_2, path)



	def _generate_different_pairs(self, pair_number):
		# Generate the different pair folders using random chosen images
				
		# Create 'different' folder in output_dir
		path = os.path.join(self.outputs_dir, 'different')
		
		try:  
    			os.mkdir(path)  
		except OSError as error:  
    			print(error)
		
		# Generate different pairs in the same number of same pairs 
		count = 0
		while (count < pair_number):

			print(count)			

			# Choose random images
			index_id = random.choice(os.listdir(self.index_dir))
			others_id = random.choice(os.listdir(self.others_dir))
			
			folder_name = "different " + index_id.split('.')[0] + ' & ' + others_id.split('.')[0]			

			path = os.path.join(self.outputs_dir + '/different', folder_name) 			

			# Check if chosen images are different and this pair was not created before (the folder was not created)
			if ((index_id.split('.')[0] is not others_id.split('_')[0]) &
				(not os.path.isdir(path))):
				
				self._make_folder(index_id, others_id, 'different', index_id)
				count = count + 1
	

def main(args):

	# Get the user directories
	parser = argparse.ArgumentParser()
	parser.add_argument("-i", "--index", help="Your index folder directory.")
	parser.add_argument("-o", "--others", help="Your others folder directory.")
	parser.add_argument("-n", "--output", help="Your destination output folder directory.")
	args = parser.parse_args()

	# Check if user's missed one of the directories
	if(args.index and args.others and args.output) != None:
		generatePairs = GeneratePairs(args.index, args.others, args.output)
		generatePairs.generate()

	else:
		print("\nYou should enter three directories for index, others and output")



if __name__ == '__main__':
	main(sys.argv)
