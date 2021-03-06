import numpy as np
import zipfile
import os

class LoadSurface():
    def loadsurfdata(self, directory, use_subcort=False):
        '''
        Pass in directory for where the entire metadata for this patient is
        '''
        # Shift to account for 0 - unknown region, not included later
        reg_map_cort = np.genfromtxt(
            (os.path.join(
                directory,
                "region_mapping_cort.txt")),
            dtype=int) - 1
        with zipfile.ZipFile(os.path.join(directory, "surface_cort.zip")) as zip:
            with zip.open('vertices.txt') as fhandle:
                verts_cort = np.genfromtxt(fhandle)
            with zip.open('normals.txt') as fhandle:
                normals_cort = np.genfromtxt(fhandle)
            with zip.open('triangles.txt') as fhandle:
                triangles_cort = np.genfromtxt(fhandle, dtype=int)
        vert_areas_cort = self._compute_vertex_areas(
            verts_cort, triangles_cort)

        if use_subcort == False:
            print('NOT USING SUBCORT')
            self.vertices = verts_cort
            self.normals = normals_cort
            self.areas = vert_areas_cort
            self.regmap = reg_map_cort
            return (verts_cort, normals_cort, vert_areas_cort, reg_map_cort)
        else:
            reg_map_subc = np.genfromtxt(
                (os.path.join(
                    directory,
                    "region_mapping_subcort.txt")),
                dtype=int) - 1
            with zipfile.ZipFile(os.path.join(directory, "surface_subcort.zip")) as zip:
                with zip.open('vertices.txt') as fhandle:
                    verts_subc = np.genfromtxt(fhandle)
                with zip.open('normals.txt') as fhandle:
                    normals_subc = np.genfromtxt(fhandle)
                with zip.open('triangles.txt') as fhandle:
                    triangles_subc = np.genfromtxt(fhandle, dtype=int)
            vert_areas_subc = self._compute_vertex_areas(
                verts_subc, triangles_subc)

            verts = np.concatenate((verts_cort, verts_subc))
            normals = np.concatenate((normals_cort, normals_subc))
            areas = np.concatenate((vert_areas_cort, vert_areas_subc))
            regmap = np.concatenate((reg_map_cort, reg_map_subc))
            self.vertices = verts
            self.normals = normals
            self.areas = areas
            self.regmap = regmap
            return (verts, normals, areas, regmap)

    def __compute_triangle_areas(self, vertices, triangles):
        """Calculates the area of triangles making up a surface."""
        tri_u = vertices[triangles[:, 1], :] - vertices[triangles[:, 0], :]
        tri_v = vertices[triangles[:, 2], :] - vertices[triangles[:, 0], :]
        tri_norm = np.cross(tri_u, tri_v)
        triangle_areas = np.sqrt(np.sum(tri_norm ** 2, axis=1)) / 2.0
        triangle_areas = triangle_areas[:, np.newaxis]
        return triangle_areas

    def _compute_vertex_areas(self, vertices, triangles):
        triangle_areas = self.__compute_triangle_areas(vertices, triangles)
        vertex_areas = np.zeros((vertices.shape[0]))
        for triang, vertices in enumerate(triangles):
            for i in range(3):
                vertex_areas[vertices[i]] += 1. / 3. * triangle_areas[triang]
        return vertex_areas
