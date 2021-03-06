require "csv"
require "rake/clean"

datasets = CSV.table "datasets.csv"
segmentation_datasets = CSV.table "segmentation_datasets.csv"

namespace :segmentation do

  segmentation_datasets.each do |dataset|

    desc "segment #{dataset[:reconstruction]}"
    file dataset[:segmentation] => ["segment.py", "segment_macro.py", dataset[:reconstruction]] do |f|
      mkdir_p dataset[:segmentation]
      sh "rm -f #{f.name}/*.tif"
      sh "python #{f.prerequisites[0]} #{f.prerequisites[2]} #{f.name}"
    end
  end

  desc "segment all"
  task :all => segmentation_datasets[:segmentation]

end

namespace :fiji do
  # test with a small file
  datasets.each do |dataset|

    desc "calculate distance ridge of #{dataset[:stitched]} with fiji"
    file dataset[:distance_map] => ["distance_map.py", "distance_map_macro.py", dataset[:stitched]] do |f|
      p "python #{f.prerequisites[0]} #{f.prerequisites[2]} #{f.name}"
      mkdir_p File.dirname(dataset[:distance_ridge])
      sh "python #{f.prerequisites[0]} #{f.prerequisites[2]} #{f.name}"
    end

    desc "calculate distance ridge of #{dataset[:distance_map]} with fiji"
    file dataset[:distance_ridge] => ["distance_ridge.py", "distance_ridge_macro.py", dataset[:distance_map]] do |f|
      p "python #{f.prerequisites[0]} #{f.prerequisites[2]} #{f.name}"
      mkdir_p File.dirname(dataset[:distance_ridge])
      sh "python #{f.prerequisites[0]} #{f.prerequisites[2]} #{f.name}"
    end

  end

  desc "distance ridges"
  task :ridge => datasets[:distance_ridge]

  desc "distance map"
  task :map => datasets[:distance_map]

end

namespace :compression do

  datasets.each do |dataset|

    desc "compress local thickness of #{dataset[:name]}"
    file dataset[:thickness_map_compressed] => ["compress.py", dataset[:thickness_map]] do |f|
      #sh "python #{f.prerequisites[0]} --chunks 25 #{f.prerequisites[1]} #{f.name}"
      sh "srun python #{f.prerequisites[0]} #{f.prerequisites[1]} #{f.name}"
    end

    #desc "plot local thickness of #{dataset[:name]}"
    #file dataset[:local_thickness_plot] => ["plot_single.R", dataset[:local_thickness_kde]] do |f|
      #sh "./#{f.prerequisites[0]} --title #{dataset[:name]} #{f.prerequisites[1]} #{f.name}"
    #end

    desc "compression"
    task :all => datasets[:thickness_map_compressed]

  end

end

namespace :kde do

  datasets.each do |dataset|

    desc "calculate kde of #{dataset[:name]}"
    file dataset[:kde] => ["thickmap2kde.R", dataset[:thickness_map_compressed_local]] do |f|
      sh "./#{f.prerequisites[0]} #{f.prerequisites[1]} #{f.name} --xmax 100"
    end

  end

  desc "kde"
  task :all => datasets[:kde]

end
