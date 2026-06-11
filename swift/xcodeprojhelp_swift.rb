require 'xcodeproj'

def add_swift_reference(projpath, projname, filename, filepath)
  project = Xcodeproj::Project.open(projpath)

  target_index = nil
  target_index_clean = nil

  project.targets.each_with_index do |target, index|
    target_index = index if target.name == projname
    target_index_clean = index if target.name == "#{projname}_CLEAN"
  end

  raise "Target not found: #{projname}" if target_index.nil?

  target = project.targets[target_index]
  group = project.main_group.find_subpath(File.join(projname), true)
  group.set_source_tree('SOURCE_ROOT')

  swift_path = filepath + filename + '.swift'
  file_ref = group.new_reference(swift_path)
  target.add_file_references([file_ref])

  unless target_index_clean.nil?
    target_clean = project.targets[target_index_clean]
    target_clean.add_file_references([file_ref])
  end

  project.save
end

add_swift_reference(ARGV[0], ARGV[1], ARGV[2], ARGV[3])
